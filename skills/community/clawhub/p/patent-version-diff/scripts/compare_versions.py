"""Produce a line-based change table and escaped, fully offline HTML view."""
import argparse
import difflib
import html
import json
from local_table import read_text,output_dir,write_csv,write_json

def compare(old,new,out_dir):
    old_path,old_text=read_text(old);new_path,new_text=read_text(new)
    if not old_text.strip() or not new_text.strip():raise ValueError('Both inputs must contain text.')
    a=old_text.splitlines();b=new_text.splitlines()
    if max(len(a),len(b))>2000:raise ValueError('Split corresponding sections into at most 2000 lines per side.')
    rows=[];parts=[];opcodes=difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes()
    for tag,i,j,k,l in opcodes:
        left='\n'.join(a[i:j]);right='\n'.join(b[k:l])
        old_range=f'{i+1}—{j}' if i!=j else '—';new_range=f'{k+1}—{l}' if k!=l else '—'
        parts.append(f'<tr class="{tag}"><td>{old_range}<pre>{html.escape(left)}</pre></td><td>{new_range}<pre>{html.escape(right)}</pre></td></tr>')
        if tag!='equal':
            rows.append({'变更块':len(rows)+1,'类型':{'insert':'新增','delete':'删除','replace':'替换'}[tag],
                '旧版起始行':i+1 if i!=j else '','旧版结束行':j if i!=j else '',
                '新版起始行':k+1 if k!=l else '','新版结束行':l if k!=l else '',
                '旧文':left,'新文':right})
    page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>专利文本版本对照</title><style>body{font-family:system-ui;margin:24px;color:#25343b}table{width:100%;table-layout:fixed;border-collapse:collapse}td,th{border:1px solid #ccd3d7;padding:12px;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}.insert{background:#edf7ee}.delete{background:#fbecec}.replace{background:#fff5df}th{background:#eef2f5}</style>'
    page+='<h1>文本版本对照</h1><p>行号对应输入文本；仅展示文字差异，不作法律判断。换行统一为LF，其他空格与字符保留。</p>'
    page+='<table><thead><tr><th>'+html.escape(str(old_path))+'</th><th>'+html.escape(str(new_path))+'</th></tr></thead><tbody>'+''.join(parts)+'</tbody></table></html>'
    directory=output_dir(out_dir)
    write_csv(directory/'专利版本差异.csv',['变更块','类型','旧版起始行','旧版结束行','新版起始行','新版结束行','旧文','新文'],rows)
    (directory/'对照.html').write_text(page,encoding='utf8')
    stats=dict(change_blocks=len(rows),old_lines=len(a),new_lines=len(b),api_calls=0,old_source=str(old_path),new_source=str(new_path),comparison='line-based; CRLF/CR normalized on reading')
    write_json(directory/'统计.json',stats);return stats

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--old',required=True);p.add_argument('--new',required=True);p.add_argument('--out-dir',required=True)
    a=p.parse_args();print(json.dumps(compare(a.old,a.new,a.out_dir),ensure_ascii=False))
