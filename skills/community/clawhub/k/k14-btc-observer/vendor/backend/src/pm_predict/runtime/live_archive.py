"""Bounded asynchronous audit queue; one disk writer, sealed minute segments."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import threading
import time
import orjson
from pm_predict.runtime.capture_policy import storage_limit_reached


class LiveArchive:
    def __init__(self, directory, run_id, max_bytes, min_free):
        self.directory=Path(directory); self.directory.mkdir(parents=True,exist_ok=True)
        self.run_id=run_id; self.queue=queue.Queue(16384)
        self.max_bytes=max_bytes;self.min_free=min_free
        self.error=None;self.count=0;self.committed=0;self.bytes=0;self.last_commit_ms=None
        self.thread=threading.Thread(target=self._write,daemon=True,name='public-feed-audit')
        self.thread.start()

    def add(self, kind, payload, epoch=None, frame=None, received=None):
        if self.error: raise RuntimeError(self.error)
        wall,mono = received or (time.time_ns()//1_000_000,time.perf_counter_ns())
        self.count+=1
        item={'record':self.count,'run_id':self.run_id,'kind':kind,'receive_ms':wall,
              'receive_monotonic_ns':mono,'monotonic_clock':'perf_counter_ns','connection':epoch,'frame':frame,'payload':payload}
        try:self.queue.put_nowait(item)
        except queue.Full:
            self.error='raw audit queue full; unpersisted tail UNKNOWN'
            raise RuntimeError(self.error)

    def _write(self):
        raw=compressed=None; path=None; slot=None; first=None;last=None;previous=None
        last_flush=time.monotonic();last_limit=0
        total=sum(p.stat().st_size for p in self.directory.rglob('*') if p.is_file())
        def close_segment():
            nonlocal raw,compressed,previous,total
            if not raw:return
            compressed.close();raw.flush();os.fsync(raw.fileno());raw.close()
            final=path.with_suffix('');path.replace(final)
            with final.open('rb') as source:
                digest=hashlib.file_digest(source,'sha256').hexdigest()
            seal={'run_id':self.run_id,'first':first,'last':last,'sha256':digest,'previous':previous}
            final.with_suffix('.seal.json').write_text(json.dumps(seal),encoding='utf8')
            previous=digest;total+=final.stat().st_size;raw=compressed=None
        try:
            while True:
                try:item=self.queue.get(timeout=.25)
                except queue.Empty:item='FLUSH'
                if item is None:break
                if time.monotonic()-last_limit>10:
                    last_limit=time.monotonic()
                    if storage_limit_reached(total+(raw.tell() if raw else 0),self.max_bytes,
                                             shutil.disk_usage(self.directory).free,self.min_free):
                        raise RuntimeError('capture storage budget reached')
                if item != 'FLUSH':
                    new_slot=item['receive_ms']//60000
                    if new_slot != slot:
                        close_segment();slot=new_slot;first=item['record']
                        path=self.directory/f'{slot}_{self.run_id}.jsonl.gz.part'
                        raw=path.open('xb');compressed=gzip.GzipFile(fileobj=raw,mode='wb',compresslevel=1)
                    encoded=orjson.dumps(item)+b'\n';compressed.write(encoded)
                    self.bytes+=len(encoded);last=item['record']
                if raw and time.monotonic()-last_flush>=1:
                    compressed.flush();raw.flush();os.fsync(raw.fileno())
                    self.committed=last;self.last_commit_ms=time.time_ns()//1_000_000
                    last_flush=time.monotonic()
            close_segment();self.committed=last or 0
        except Exception as ex:
            self.error=f'{type(ex).__name__}: {ex}'
            if raw:
                try:compressed.close();raw.close()
                except Exception:pass

    def close(self):
        self.queue.put(None,timeout=2);self.thread.join(10)
        if self.thread.is_alive():self.error='archive close timed out; tail UNKNOWN'

    def status(self):
        return {'received':self.count,'durable':self.committed,'pending':self.queue.qsize(),
                'raw_bytes':self.bytes,'last_commit_ms':self.last_commit_ms,'error':self.error}
