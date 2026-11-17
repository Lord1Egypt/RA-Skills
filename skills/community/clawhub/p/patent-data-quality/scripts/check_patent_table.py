"""Flag internal CSV issues without claiming patent-data authenticity."""
import argparse
import datetime
import json
import re
import unicodedata
from local_table import read_table,output_dir,write_csv,write_json

def full_date(value):
    value=value.strip()
    if not value:return None,'empty'
    partial=re.fullmatch(r'(\d{4})(?:(?:[-/.]|年)(\d{1,2})月?)?',value)
    if partial:
        try:datetime.date(int(partial[1]),int(partial[2] or 1),1)
        except ValueError:return None,'invalid'
        return None,'partial'
    match=re.fullmatch(r'(\d{4})(?:[-/.]|年)(\d{1,2})(?:[-/.]|月)(\d{1,2})日?',value)
    if not match:return None,'unknown'
    try:return datetime.date(*map(int,match.groups())),'full'
    except ValueError:return None,'invalid'

def check(path,out_dir,required=None,date_columns=None,number_column='公开号'):
    required=required if required is not None else ['公开号','标题','申请人','公开日']
    date_columns=date_columns if date_columns is not None else ['申请日','公开日']
    source,fields,records=read_table(path);issues=[];raw=[];seen={}
    def issue(line,field,value,rule,level,hint):
        issues.append({'来源行号':line,'字段':field,'原值':value,'规则':rule,'级别':level,'核对建议':hint})
    for field in required:
        if field not in fields:issue(0,field,'','缺少必填列','需补资料','确认字段映射或向数据提供方索取，不自动造值')
    for line,row in records:
        raw.append({'来源行号':line,'原始数据JSON':json.dumps(row,ensure_ascii=False)})
        for field in required:
            if field in fields and not row[field].strip():issue(line,field,row[field],'必填值为空','需补资料','回查原始来源，不凭常识补值')
        pn=re.sub(r'\s+','',unicodedata.normalize('NFKC',row.get(number_column,'')).upper())
        if pn:
            if not re.fullmatch(r'(?!ZL)[A-Z]{2}\d{4,14}(?:\.\d+)?[A-Z]\d{0,2}',pn):
                issue(line,number_column,row[number_column],'号码格式需核对','待复核','核对是否为完整公开号、种类码或其他历史格式；此处不验证真实性')
            if pn in seen:issue(line,number_column,row[number_column],'重复完整标识','待复核',f'与来源行{seen[pn]}相同；不自动删行、不归并A/B或同族')
            else:seen[pn]=line
        parsed={}
        for field in date_columns:
            if field not in fields:continue
            date,status=full_date(row[field]);parsed[field]=date
            if status=='partial':issue(line,field,row[field],'日期精度不足','说明项','保留年或年月精度，不补成月初或年初')
            elif status=='invalid':issue(line,field,row[field],'日历日期无效','待复核','回查原始日期、OCR及字段映射')
            elif status=='unknown':issue(line,field,row[field],'日期格式待核对','待复核','确认实际格式后再解析，不擅自改变日期')
        if parsed.get('申请日') and parsed.get('公开日') and parsed['公开日']<parsed['申请日']:
            issue(line,'申请日/公开日',row['申请日']+' / '+row['公开日'],'日期先后待核对','待复核','确认是否同一公开文本及是否混入优先权日、授权日或其他口径')
    directory=output_dir(out_dir)
    write_csv(directory/'专利数据质检问题.csv',['来源行号','字段','原值','规则','级别','核对建议'],issues)
    write_csv(directory/'原始数据明细.csv',['来源行号','原始数据JSON'],raw)
    stats=dict(records=len(records),issues=len(issues),affected_rows=len({r['来源行号'] for r in issues if r['来源行号']}),
        table_level_issues=sum(r['来源行号']==0 for r in issues),required_columns=required,date_columns=date_columns,
        number_column=number_column,api_calls=0,source=str(source),meaning='Internal checks only; no authenticity or legal-status verification.')
    write_json(directory/'统计.json',stats);return stats

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--out-dir',required=True)
    p.add_argument('--required',nargs='+',default=None);p.add_argument('--date-columns',nargs='+',default=None);p.add_argument('--number-column',default='公开号')
    a=p.parse_args();print(json.dumps(check(a.input,a.out_dir,a.required,a.date_columns,a.number_column),ensure_ascii=False))
