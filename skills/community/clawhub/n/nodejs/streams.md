# Streams — Backpressure, Pipelines, and Transforms

The reason to use a stream is constant memory: the process holds one buffer, not one file. Every trap below is a way of accidentally giving that up.

## Backpressure

- highWaterMark defaults: 16 KiB (generic streams), 64 KiB (`fs.createReadStream`), 16 items (objectMode). Raising it trades memory for fewer syscalls — a bulk file copy at 1 MiB does ~16× fewer reads than at 64 KiB; memory cost = highWaterMark × concurrent streams.
- `write()` returning false means the internal buffer passed highWaterMark. Ignoring it works — until sustained load buffers the entire source in RAM. Pattern: `if (!w.write(chunk)) await once(w, 'drain')`.
- Backpressure is per-link, and one link that ignores it defeats the whole chain: a transform that pushes everything it receives regardless of `push()`'s return value converts a streaming pipeline back into a buffering one.
- Symptom of lost backpressure: RSS tracks the size of the input rather than staying flat. That is the check — run the job against a file 10× larger and watch whether memory moves.
- Reading faster than the destination writes is normal and fine; reading faster than the destination *and* buffering the difference in an array of your own is the bug.

## Pipelines

- `.pipe()` neither forwards errors nor cleans up on failure — `pipeline(src, ...transforms, dst)` does both, and accepts async generators as transforms (the modern way to write a one-off Transform).
- `pipeline` from `node:stream/promises` returns a promise: `await pipeline(a, b, c)`, one try/catch for the whole chain, all streams destroyed on failure.
- Pass `{ signal }` to `pipeline` to make the whole chain cancellable — the right way to abandon a large export when the client disconnects (→ `async.md`).
- Any stream outside a pipeline needs its own `'error'` handler — an unhandled stream `'error'` is a process crash, not a rejected promise.
- `end()` vs `destroy()`: end flushes buffered data then closes; destroy drops it. Error paths want destroy (pipeline calls it for you) — calling end on error can flush half-written garbage downstream.
- A pipeline that resolves is not proof the data landed: with a filesystem destination, `finish` means the bytes reached the OS. Durability needs an fsync (→ `filesystem.md`).

## Consuming

- `for await (const chunk of readable)` respects backpressure automatically; but `break`/`throw` inside the loop destroys the stream — you cannot resume it later.
- Don't mix consumption modes: attaching `on('data')` switches the stream to flowing mode and races against pipe or async-iterator consumers of the same stream.
- Two consumers of one readable split the data; they do not each get a copy. To fan out, tee explicitly by writing to both destinations from one loop, and let the slower destination apply backpressure to both.
- A paused readable that nobody resumes holds its descriptor and its buffer indefinitely — a common leak when an early `return` skips the consumption path.
- Convenience over correctness where the size is known and small: `await text(readable)` / `await buffer(readable)` from `node:stream/consumers` are readable and honest about buffering everything. Never on input whose size a user controls.

## Writing Transforms

```js
import { pipeline } from 'node:stream/promises';
await pipeline(
  createReadStream('in.ndjson'),
  async function* (source) {                 // async generator = Transform, with backpressure for free
    source.setEncoding('utf8');
    let tail = '';
    for await (const chunk of source) {
      const lines = (tail + chunk).split('\n');
      tail = lines.pop();                    // the incomplete last line belongs to the next chunk
      for (const line of lines) if (line) yield JSON.stringify(transform(JSON.parse(line))) + '\n';
    }
    if (tail) yield JSON.stringify(transform(JSON.parse(tail))) + '\n';
  },
  createWriteStream('out.ndjson'),
);
```

- Chunk boundaries are arbitrary: they split multi-byte UTF-8 characters, JSON lines, and CSV rows. Either `setEncoding('utf8')` (which buffers partial characters for you) or carry a tail across iterations, as above. Assuming one chunk = one record is the single most common streaming bug.
- objectMode counts items, not bytes: 16 objects of 10 MB each is 160 MB of buffer at the default highWaterMark. Size it deliberately for large objects.
- A Transform that awaits a slow call per chunk serializes the whole pipeline. Batch the calls, or cap parallelism inside the transform (SKILL.md rule 4) rather than removing the stream.
- Errors inside an async generator transform propagate to `pipeline` — no callback plumbing, no swallowed rejection.

## Buffers and Encodings

- Buffers live outside the V8 heap: they count against RSS and the container limit but not `--max-old-space-size` (SKILL.md rule 8). A "leak" that heap snapshots cannot see is usually buffers held in a cache.
- `Buffer.alloc(n)` zero-fills; `Buffer.allocUnsafe(n)` hands back pooled memory that may contain previous data — safe only if you overwrite every byte before anything reads it.
- `Buffer.byteLength(str)` is not `str.length` for anything non-ASCII. Size checks and `Content-Length` computed from string length are wrong by exactly the multi-byte characters (→ `http.md`).
- Accumulate chunks in an array and `Buffer.concat` once. `buf = Buffer.concat([buf, chunk])` per chunk copies the whole accumulation every time — quadratic, and the usual reason a "streaming" upload handler pins a core.
- `subarray`/`slice` shares memory with the parent: keeping a 10-byte header out of a 10 MB read retains all 10 MB. Copy the bytes you intend to keep.
- Multi-byte characters split across chunks: `new TextDecoder('utf8')` with `{ stream: true }` per chunk buffers the partial sequence, which is what `setEncoding('utf8')` does internally.
- base64 grows payloads by ~33%: decoding untrusted base64 without a length cap is a memory amplification attack (→ `security.md`).

## Interop

- Node streams and Web streams convert both ways: `Readable.fromWeb`/`Readable.toWeb` and their Writable counterparts. `fetch` bodies are Web streams, so a proxying handler needs one conversion at each boundary (→ `http.md`).
- `Readable.from(iterable)` turns an array, generator, or async generator into a stream — the cheap way to give a batch API a streaming interface.
- HTTP requests and responses are streams: a client disconnect mid-response errors the destination, which is another reason handlers use `pipeline`, not `pipe`.
- zlib streams hold native memory until destroyed; a compression stream abandoned on an error path leaks outside the JS heap and will not appear in a heap snapshot (→ `performance.md`).
- Database drivers with a cursor/stream mode keep memory constant on large result sets — the same principle, and usually the actual fix when an export OOMs.
