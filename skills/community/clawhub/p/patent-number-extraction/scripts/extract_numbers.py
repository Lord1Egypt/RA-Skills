"""Extract syntactic patent-number candidates with original-text locations."""
import argparse
import bisect
import collections
import json
import re
import unicodedata
from local_table import read_text,output_dir,write_csv,write_json

PUBLICATION=re.compile(r'(?<![A-Z0-9])(?P<country>(?!ZL)[A-Z]{2})[ \t]*(?P<digits>\d[\d \t/]{3,24}?)[ \t]*(?P<kind>[A-Z]\d{0,2})(?![A-Z0-9])')
APPLICATION=re.compile(r'(?<![A-Z0-9])(?:ZL|CN)[ \t]*\d{12}\.[0-9X](?![A-Z0-9])')

def extract(path,out_dir):
    source,text=read_text(path);shadow=[];positions=[]
    for index,ch in enumerate(text):
        converted=unicodedata.normalize('NFKC',ch).upper()
        shadow.append(converted);positions.extend([index]*len(converted))
    normalized=''.join(shadow);newlines=[i for i,ch in enumerate(text) if ch=='\n']
    matches=[]
    for pattern,kind in [(PUBLICATION,'公开号候选（仅格式识别）'),(APPLICATION,'中国申请号候选（未校验）')]:
        for match in pattern.finditer(normalized):
            candidate=re.sub(r'[ \t/]','',match.group())
            if pattern is PUBLICATION and not 4<=len(re.sub(r'\D','',match.group('digits')))<=14:continue
            start=positions[match.start()];end=positions[match.end()-1]+1
            line_index=bisect.bisect_right(newlines,start)
            matches.append({'原文号码':text[start:end],'规范候选':candidate,'号码类型':kind,
                '文本行号':line_index+1,'列号':start-(newlines[line_index-1] if line_index else -1),
                '起始字符':start,'结束字符':end,'上下文':text[max(0,start-45):min(len(text),end+45)],
                '来源文件':str(source),'核验状态':'未联网核验'})
            if len(matches)>10000:raise ValueError('More than 10000 occurrences; split the source by section.')
    matches.sort(key=lambda row:row['起始字符'])
    counts=collections.Counter(row['规范候选'] for row in matches)
    directory=output_dir(out_dir)
    fields=['原文号码','规范候选','号码类型','文本行号','列号','起始字符','结束字符','上下文','来源文件','核验状态']
    write_csv(directory/'专利号码出处表.csv',fields,matches)
    write_csv(directory/'号码索引.csv',['规范候选','出现次数'],[{'规范候选':k,'出现次数':v} for k,v in counts.items()])
    stats=dict(occurrences=len(matches),unique_candidates=len(counts),api_calls=0,
        location='Offsets are zero-based Unicode character offsets [start,end); line and column are one-based in the extracted UTF-8 text.',
        limitations='Syntactic candidates only; country/kind codes, check digits, existence and historical numbering formats are not validated.')
    write_json(directory/'统计.json',stats);return stats

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--out-dir',required=True)
    a=p.parse_args();print(json.dumps(extract(a.input,a.out_dir),ensure_ascii=False))
