"""Build a traceable reading bibliography, without claiming a citation standard."""
import argparse
import json
from local_table import read_table,output_dir,write_csv,write_json,escape_md

def bibliography(path,out_dir,number='公开号',title='标题',date='公开日',applicant='申请人',responsible='责任者'):
    source,fields,records=read_table(path);rows=[];raw=[];seen=set();duplicates=0
    for index,(line,row) in enumerate(records,1):
        pn=row.get(number,'').strip();name=row.get(title,'').strip();published=row.get(date,'').strip()
        owner=row.get(applicant,'').strip();author=row.get(responsible,'').strip()
        missing=[label for label,value in [('公开号',pn),('标题',name),('公开日',published),('申请人',owner)] if not value]
        entry=f"[{index}] {name or '[标题缺失]'} [专利]. {pn or '[公开号缺失]'}. 公开日：{published or '[缺失]'}. 申请人：{owner or '[缺失]'}。"
        if pn and pn in seen:duplicates+=1
        if pn:seen.add(pn)
        rows.append({'序号':index,'公开号':pn,'标题':name,'公开日':published,'申请人':owner,'责任者原文':author,
            '引用条目':entry,'缺失字段':'、'.join(missing),'来源文件':str(source),'来源行号':line})
        raw.append({'来源行号':line,'原始数据JSON':json.dumps(row,ensure_ascii=False)})
    directory=output_dir(out_dir)
    write_csv(directory/'专利文献引用表.csv',['序号','公开号','标题','公开日','申请人','责任者原文','引用条目','缺失字段','来源文件','来源行号'],rows)
    write_csv(directory/'原始数据明细.csv',['来源行号','原始数据JSON'],raw)
    content='# 专利引用清单\n\n通用阅读格式，未按某项国标或期刊规则认证；申请人不自动视为作者。\n\n'
    content+='\n\n'.join(escape_md(row['引用条目']) for row in rows)
    (directory/'引用清单.md').write_text(content+'\n',encoding='utf8')
    stats=dict(records=len(rows),rows_with_missing_fields=sum(bool(r['缺失字段']) for r in rows),
        duplicate_identifiers=duplicates,source=str(source),api_calls=0,format='numbered reading bibliography')
    write_json(directory/'统计.json',stats);return stats

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--out-dir',required=True)
    for option,default in [('number','公开号'),('title','标题'),('date','公开日'),('applicant','申请人'),('responsible','责任者')]:
        p.add_argument('--'+option+'-column',default=default)
    a=p.parse_args();print(json.dumps(bibliography(a.input,a.out_dir,a.number_column,a.title_column,a.date_column,a.applicant_column,a.responsible_column),ensure_ascii=False))
