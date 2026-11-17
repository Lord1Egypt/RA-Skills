"""Offline CSV grouping by complete publication number; never drops source rows."""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path


def normalize(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value)).upper()


def group_csv(inputs, column, output):
    paths = [Path(p).resolve(strict=True) for p in inputs]
    # Read and validate all sources before creating output.
    records = []
    for path in paths:
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            names = reader.fieldnames
            if not names or column not in names or len(names) != len(set(names)):
                raise ValueError(f'Column missing or duplicate header: {path}')
            for row in reader:
                line = reader.line_num
                if None in row or any(v is None for v in row.values()):
                    raise ValueError(f'Malformed CSV record: {path}, line {line}')
                records.append((path, line, row))
    output = Path(output).resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Output directory must be empty or absent')
    output.mkdir(parents=True, exist_ok=True)
    groups, details = {}, []
    for index, (path, line, row) in enumerate(records, 1):
        number = normalize(row[column])
        # Conservative syntactic grouping only; no existence/family inference.
        valid = bool(re.fullmatch(r'[A-Z]{2}\d{4,14}(?:\.\d+)?[A-Z]\d{0,2}', number))
        key = number if valid else f'UNRESOLVED_{index}'
        group = groups.setdefault(key, {'id': f'G{len(groups)+1:05d}', 'number': number if valid else '',
            'valid': valid, 'rows': []})
        item = {'组号': group['id'], '规范公开号': number if valid else '', '来源文件': str(path),
                '来源行号': line, '原始数据JSON': json.dumps(row, ensure_ascii=False),
                '待核实': '' if valid else '缺号或格式不明确，独立保留'}
        group['rows'].append((row, item))
        details.append(item)
    conflicts, summary = [], []
    for group in groups.values():
        rows = group['rows']
        fields = dict.fromkeys(k for row, _ in rows for k in row if k != column)
        conflict_fields = []
        for field in fields:
            values = list(dict.fromkeys(row.get(field, '') for row, _ in rows
                                        if row.get(field, '') != ''))
            if len(values) > 1:
                conflict_fields.append(field)
                conflicts.append({'组号': group['id'], '规范公开号': group['number'],
                    '字段': field, '不同原始值JSON': json.dumps(values, ensure_ascii=False),
                    '核对': '首见值不代表正确值；见原始明细逐条来源'})
        first_row, first = rows[0]
        summary.append({'组号': group['id'], '规范公开号': group['number'],
            '首见记录': json.dumps(first_row, ensure_ascii=False),
            '来源文件': first['来源文件'], '来源行号': first['来源行号'],
            '是否有冲突': '是：'+','.join(conflict_fields) if conflict_fields else '否',
            '待核实': first['待核实']})

    def write(name, names, rows):
        with (output/name).open('w', encoding='utf-8-sig', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=names)
            writer.writeheader()
            writer.writerows(rows)

    write('专利合并清单.csv', ['组号','规范公开号','首见记录','来源文件','来源行号','是否有冲突','待核实'], summary)
    write('原始明细.csv', ['组号','规范公开号','来源文件','来源行号','原始数据JSON','待核实'], details)
    write('字段冲突.csv', ['组号','规范公开号','字段','不同原始值JSON','核对'], conflicts)
    stats = {'input_rows': len(records), 'output_groups': len(groups),
        'duplicate_rows': len(records)-len(groups),
        'unresolved_rows': sum(not group['valid'] for group in groups.values()),
        'conflict_fields': len(conflicts), 'api_calls': 0}
    (output/'统计.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf8')
    return stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', nargs='+', required=True)
    parser.add_argument('--column', default='公开号')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    print(json.dumps(group_csv(args.inputs, args.column, args.out_dir), ensure_ascii=False))
