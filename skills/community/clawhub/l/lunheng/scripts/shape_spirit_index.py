#!/usr/bin/env python3
"""
《形与神》混合检索工具
- 索引层：快速检索案例编号、关键词、案由
- 内容层：按需从 PDF 提取详细内容
"""
import json
import re
from pathlib import Path
from typing import Optional
import pdfplumber

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "shape_spirit"
LEARNINGS_DIR = SKILL_DIR / "learnings"

PDF_FILES = {
    "civil": "双百优秀裁判文书的形与神：裁判思路与说理技巧（民事卷） (最高人民法院审判管理办公室) .pdf",
    "criminal": "双百优秀裁判文书的形与神：裁判思路与说理技巧（刑事卷） (最高人民法院审判管理办公室).pdf",
    "commercial": "双百优秀裁判文书的形与神：裁判思路与说理技巧（商事，海事海商，知识产权卷） (最高人民法院审判管理办公室).pdf",
    "administrative": "双百优秀裁判文书的形与神：裁判思路与说理技巧（行政，国家赔偿，执行卷） (最高人民法院审判管理办公室).pdf",
}

# 案由分类映射
CAUSE_MAP = {
    "civil": {
        "人格权": ["生命权", "健康权", "身体权", "姓名权", "名誉权", "隐私权", "个人信息"],
        "婚姻家庭": ["离婚", "抚养", "赡养", "探望权", "监护权"],
        "继承": ["法定继承", "遗嘱继承", "遗赠"],
        "所有权": ["物权确认", "返还原物", "排除妨害", "共有"],
        "劳动争议": ["劳动合同", "工伤", "经济补偿", "赔偿金"],
        "买卖合同": ["买卖", "退货", "质量", "交付"],
        "借款合同": ["民间借贷", "金融借款", "利息", "担保"],
        "租赁合同": ["房屋租赁", "设备租赁"],
        "承揽合同": ["加工", "定作", "修理"],
        "建设工程": ["施工合同", "工程款", "质量"],
        "服务合同": ["服务", "委托", "中介"],
        "保理合同": ["保理", "应收账款"],
        "侵权责任": ["交通事故", "医疗损害", "产品责任", "环境污染"],
    },
    "criminal": {
        "危害公共安全": ["放火", "爆炸", "危险驾驶", "交通肇事"],
        "经济犯罪": ["诈骗", "合同诈骗", "集资诈骗", "贷款诈骗"],
        "人身犯罪": ["故意杀人", "故意伤害", "强奸", "绑架"],
        "财产犯罪": ["抢劫", "盗窃", "抢夺", "敲诈勒索"],
        "妨害司法": ["伪证", "拒不执行"],
        "毒品犯罪": ["贩卖", "运输", "制造", "持有"],
        "贪污贿赂": ["贪污", "受贿", "挪用公款"],
    },
    "commercial": {
        "公司纠纷": ["股东资格", "股权转让", "公司决议", "公司清算"],
        "保险纠纷": ["财产保险", "人身保险", "保险理赔"],
        "海事海商": ["船舶碰撞", "海上运输", "海难救助", "海上保险"],
        "知识产权": ["著作权", "专利权", "商标权", "不正当竞争"],
    },
    "administrative": {
        "行政处罚": ["罚款", "吊销", "责令"],
        "行政许可": ["许可证", "审批"],
        "行政征收": ["土地征收", "房屋征收"],
        "行政复议": ["复议决定"],
        "行政赔偿": ["国家赔偿", "行政赔偿"],
        "执行": ["执行异议", "执行监督"],
    },
}


class ShapeSpiritIndex:
    """形与神检索工具"""
    
    def __init__(self):
        self.index = self._load_index()
        self.pdf_dir = LEARNINGS_DIR
    
    def _load_index(self) -> dict:
        """加载索引"""
        index_path = DATA_DIR / "index.json"
        if index_path.exists():
            with open(index_path) as f:
                return json.load(f)
        return {}
    
    def search_by_cause(self, cause: str, volume: str = None) -> list:
        """按案由搜索"""
        results = []
        volumes = [volume] if volume else PDF_FILES.keys()
        
        for vol in volumes:
            vol_file = DATA_DIR / f"{vol}.json"
            if not vol_file.exists():
                continue
            with open(vol_file) as f:
                data = json.load(f)
            
            for case in data.get("extracted_cases", []):
                title = case.get("title", "")
                keywords = " ".join(case.get("keywords", []))
                if cause in title or cause in keywords:
                    results.append({
                        "volume": vol,
                        "num": case["num"],
                        "title": case["title"],
                        "keywords": case.get("keywords", []),
                    })
        
        return results
    
    def search_by_keyword(self, keyword: str, volume: str = None) -> list:
        """按关键词搜索"""
        results = []
        volumes = [volume] if volume else PDF_FILES.keys()
        
        for vol in volumes:
            vol_file = DATA_DIR / f"{vol}.json"
            if not vol_file.exists():
                continue
            with open(vol_file) as f:
                data = json.load(f)
            
            for case in data.get("extracted_cases", []):
                keywords = case.get("keywords", [])
                title = case.get("title", "")
                if any(keyword in kw for kw in keywords) or keyword in title:
                    results.append({
                        "volume": vol,
                        "num": case["num"],
                        "title": case["title"],
                        "keywords": keywords,
                    })
        
        return results
    
    def get_case_summary(self, volume: str, case_num: int) -> dict:
        """获取案例摘要"""
        vol_file = DATA_DIR / f"{volume}.json"
        if not vol_file.exists():
            return {}
        
        with open(vol_file) as f:
            data = json.load(f)
        
        for case in data.get("extracted_cases", []):
            if case["num"] == case_num:
                return case
        
        return {}
    
    def get_case_full_text(self, volume: str, case_num: int) -> str:
        """从 PDF 提取案例全文（按需）"""
        pdf_filename = PDF_FILES.get(volume)
        if not pdf_filename:
            return "卷册不存在"
        
        pdf_path = self.pdf_dir / pdf_filename
        if not pdf_path.exists():
            return "PDF 文件不存在"
        
        # 获取案例摘要以确定页码范围
        summary = self.get_case_summary(volume, case_num)
        if not summary:
            return "案例不存在"
        
        # 用 pdfplumber 提取全文（保留表格结构）
        text_parts = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row:
                            page_text += "\n" + " ".join(str(c or "") for c in row)
                text_parts.append(page_text)
        full_text = "\n".join(text_parts)
        
        # 查找案例位置
        title_short = summary.get("title", "")[:15]
        pattern = rf'{case_num}[·．.]\s*{re.escape(title_short)}'
        match = re.search(pattern, full_text)
        
        if not match:
            return f"未找到案例 {case_num}"
        
        start = match.start()
        # 查找下一个案例
        next_pattern = rf'{case_num + 1}[·．.]'
        next_match = re.search(next_pattern, full_text[start + 100:])
        end = start + 100 + next_match.start() if next_match else start + 8000
        
        return full_text[start:end]
    
    def list_all_cases(self, volume: str = None) -> list:
        """列出所有案例"""
        cases = []
        volumes = [volume] if volume else PDF_FILES.keys()
        
        for vol in volumes:
            vol_file = DATA_DIR / f"{vol}.json"
            if not vol_file.exists():
                continue
            with open(vol_file) as f:
                data = json.load(f)
            
            for case in data.get("toc_cases", []):
                cases.append({
                    "volume": vol,
                    "num": case["num"],
                    "title": case["title"],
                })
        
        return cases
    
    def get_writing_tips(self, volume: str = None) -> list:
        """提取撰写心得精华"""
        tips = []
        volumes = [volume] if volume else PDF_FILES.keys()
        
        for vol in volumes:
            vol_file = DATA_DIR / f"{vol}.json"
            if not vol_file.exists():
                continue
            with open(vol_file) as f:
                data = json.load(f)
            
            for case in data.get("extracted_cases", []):
                exp = case.get("writing_experience", "")
                if exp and len(exp) > 100:
                    tips.append({
                        "volume": vol,
                        "num": case["num"],
                        "title": case["title"],
                        "experience": exp[:500],
                    })
        
        return tips


# CLI 入口
if __name__ == "__main__":
    import sys
    
    index = ShapeSpiritIndex()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python shape_spirit_index.py list [volume]")
        print("  python shape_spirit_index.py search <keyword> [volume]")
        print("  python shape_spirit_index.py cause <案由> [volume]")
        print("  python shape_spirit_index.py case <volume> <num>")
        print("  python shape_spirit_index.py tips [volume]")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        vol = sys.argv[2] if len(sys.argv) > 2 else None
        cases = index.list_all_cases(vol)
        print(f"共 {len(cases)} 个案例:")
        for c in cases[:20]:
            print(f"  [{c['volume']}] {c['num']}. {c['title'][:60]}")
        if len(cases) > 20:
            print(f"  ... 还有 {len(cases) - 20} 个")
    
    elif cmd == "search":
        keyword = sys.argv[2] if len(sys.argv) > 2 else ""
        vol = sys.argv[3] if len(sys.argv) > 3 else None
        results = index.search_by_keyword(keyword, vol)
        print(f"关键词 '{keyword}' 匹配 {len(results)} 个案例:")
        for r in results[:10]:
            print(f"  [{r['volume']}] {r['num']}. {r['title'][:60]}")
    
    elif cmd == "cause":
        cause = sys.argv[2] if len(sys.argv) > 2 else ""
        vol = sys.argv[3] if len(sys.argv) > 3 else None
        results = index.search_by_cause(cause, vol)
        print(f"案由 '{cause}' 匹配 {len(results)} 个案例:")
        for r in results[:10]:
            print(f"  [{r['volume']}] {r['num']}. {r['title'][:60]}")
    
    elif cmd == "case":
        vol = sys.argv[2] if len(sys.argv) > 2 else "civil"
        num = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        summary = index.get_case_summary(vol, num)
        if summary:
            print(f"标题: {summary.get('title', '')}")
            print(f"关键词: {summary.get('keywords', [])}")
            print(f"案情: {summary.get('brief_facts', '')[:200]}")
            print(f"撰写心得: {summary.get('writing_experience', '')[:300]}")
        else:
            print("案例不存在")
    
    elif cmd == "tips":
        vol = sys.argv[2] if len(sys.argv) > 2 else None
        tips = index.get_writing_tips(vol)
        print(f"撰写心得精华 ({len(tips)} 条):")
        for t in tips[:5]:
            print(f"\n[{t['volume']}] {t['num']}. {t['title'][:50]}")
            print(f"  {t['experience'][:200]}...")
    
    else:
        print(f"未知命令: {cmd}")
