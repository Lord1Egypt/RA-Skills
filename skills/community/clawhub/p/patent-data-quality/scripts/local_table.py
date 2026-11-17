"""Small UTF-8 file helpers. No network, credentials or input-file mutations."""
import csv
import json
import re
from pathlib import Path

def read_text(path):
    p=Path(path).resolve(strict=True)
    if not p.is_file() or p.stat().st_size>2*1024*1024:
        raise ValueError('Input must be a text file no larger than 2 MiB; split it by section.')
    return p,p.read_text(encoding='utf-8-sig')

def read_table(path):
    p=Path(path).resolve(strict=True)
    if p.stat().st_size>2*1024*1024:raise ValueError('Split CSV files larger than 2 MiB.')
    csv.field_size_limit(2*1024*1024)
    with p.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames
        if not fields or len(set(fields))!=len(fields):raise ValueError('Missing or duplicate CSV headers.')
        rows=[]
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'Malformed CSV record ending at line {reader.line_num}')
            rows.append((reader.line_num,row))
    return p,fields,rows

def output_dir(path):
    p=Path(path).resolve()
    p.mkdir(parents=True,exist_ok=False)
    return p

def safe_cell(value):
    if isinstance(value,str) and re.match(r'^\s*[=+@-]',value):return "'"+value
    return value

def write_csv(path,fields,rows):
    with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        writer.writerows({k:safe_cell(row.get(k,'')) for k in fields} for row in rows)

def write_json(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')

def escape_md(value):
    return re.sub(r'([\\`*{}\[\]()#+.!_<>|])',r'\\\1',str(value))
