#!/usr/bin/env python3
"""Generate a lightweight monthly checklist from pathway and target year."""
from __future__ import annotations
import argparse, json, sys

DEFAULTS = {
    '保研': ['1-3月：保绩点、补英语、整理成果', '4-6月：关注学院细则、准备夏令营材料', '7-9月：夏令营/预推免/正式推免', '9-10月：推免系统确认'],
    '考研': ['3-6月：定校定专业与基础复习', '7-9月：强化训练', '10月：报名确认', '12月：初试', '次年2-4月：复试/调剂'],
    '留学': ['提前12-18个月：语言与背景提升', '提前9-12个月：选校与文书', '提前6-9个月：递交申请', '拿到录取后：签证与行前'],
    '读博': ['提前6-12个月：联系导师与准备研究计划', '按学校公告：提交申请材料', '综合考核：笔试/面试/答辩', '拟录取后：体检、公示、调档'],
    '评职称': ['年初：核验资格年限与考核', '年中：整理业绩、论文、项目、佐证', '申报期：提交材料并公示', '评审期：答辩/同行评议/结果备案'],
    '专升本': ['省级公告前：核验资格与专业对应', '报名期：报名缴费', '考前：公共课与专业课冲刺', '录取期：志愿与录取确认'],
    '保本': ['当前学期：核学分与挂科', '下学期：补修/补考/培养方案核对', '学籍节点：确认预警与毕业资格', '毕业前：查缺补漏']
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pathway', required=True)
    ap.add_argument('--year', required=False)
    args = ap.parse_args()
    items = DEFAULTS.get(args.pathway, [])
    json.dump({'pathway': args.pathway, 'year': args.year, 'checklist': items}, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == '__main__':
    main()
