"""
智能健康管理与评估助手
前端交互与接口透传端
支持配置管理和HTML报告生成
"""

import json
import os
import re
import subprocess
import requests
import webbrowser
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path


# 模块级 API Key 缓存（进程内只请求一次）
_API_KEY_CACHE: Optional[str] = None


def _fetch_api_key() -> str:
    """通过远程接口获取 API Key，结果缓存在模块变量中"""
    global _API_KEY_CACHE
    if _API_KEY_CACHE:
        return _API_KEY_CACHE
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10",
             "https://jiyinjia.jinbaisen.com/!token?key=skill_jk"],
            capture_output=True, text=True, timeout=15
        )
        key = result.stdout.strip()
        if key:
            _API_KEY_CACHE = key
            return key
    except Exception:
        pass
    raise RuntimeError("无法获取 API Key，请检查网络连接后重试。")


class HealthAssistantConfig:
    """健康管理助手配置管理"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # 默认从技能目录加载配置
            skill_dir = Path(__file__).parent.parent
            config_path = skill_dir / "config" / "contact.json"
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if not self.config_path.exists():
            # 返回默认配置
            return {
                "screening": {
                    "name": "吉因加Geneplus健康筛查",
                    "url": "https://bms.test.geneplus.cn",
                    "description": "专业健康筛查，助您早发现、早预防、早干预"
                },
                "hotline": {
                    "number": "400-999-9999",
                    "hours": "周一至周五 9:00-18:00"
                },
                "report": {
                    "title": "健康疾病风险评估报告",
                    "subtitle": "Smart Health Risk Assessment Report",
                    "generated_by": "智能健康管理助手",
                    "powered_by": "吉因加 Geneplus"
                }
            }
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @property
    def screening_url(self) -> str:
        return self._config.get("screening", {}).get("url", "https://bms.test.geneplus.cn")
    
    @property
    def screening_name(self) -> str:
        return self._config.get("screening", {}).get("name", "吉因加Geneplus健康筛查")
    
    @property
    def screening_description(self) -> str:
        return self._config.get("screening", {}).get("description", "专业健康筛查")
    
    @property
    def hotline_number(self) -> str:
        return self._config.get("hotline", {}).get("number", "400-999-9999")
    
    @property
    def hotline_hours(self) -> str:
        return self._config.get("hotline", {}).get("hours", "周一至周五 9:00-18:00")
    
    @property
    def report_title(self) -> str:
        return self._config.get("report", {}).get("title", "健康疾病风险评估报告")
    
    @property
    def report_subtitle(self) -> str:
        return self._config.get("report", {}).get("subtitle", "Smart Health Risk Assessment Report")
    
    @property
    def powered_by(self) -> str:
        return self._config.get("report", {}).get("powered_by", "吉因加 Geneplus")


class ReportTemplate:
    """HTML报告模板管理器"""
    
    def __init__(self, template_path: str = None):
        if template_path is None:
            skill_dir = Path(__file__).parent.parent
            template_path = skill_dir / "templates" / "report_template.html"
        
        self.template_path = Path(template_path)
        self._template = self._load_template()
    
    def _load_template(self) -> str:
        """加载模板文件"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"模板文件不存在: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render(self, data: Dict) -> str:
        """渲染模板，替换占位符"""
        result = self._template
        
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        
        return result


class HealthAssistant:
    """智能健康管理助手 - 信息采集与API透传"""
    
    BASE_URL = "https://ydai.jinbaisen.com/api/v1"
    MODEL = "cyzh-cfc"
    
    OPENING_MESSAGE = """您好！我是您的智能健康管理助手。为了给您生成准确的《健康疾病风险评估报告》，请您提供以下信息：

**基础信息**（必填）：姓名、年龄、性别、所在地区、职业
**健康病史**（必填）：既往病史、家族遗传史、生活方式（吸烟、饮酒、熬夜等）
**用药与特殊状态**（必填）：当前用药史、过敏史、女性请告知生理周期状态
**检验单据**（关键）：体检单、化验单或检验单数据

请按顺序提供以上信息。"""

    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.user_info = {
            "basic": {}, 
            "medical": {}, 
            "medication": {}, 
            "lab_results": []
        }
        self.info_complete = False
        self.config = HealthAssistantConfig()
        self.template = ReportTemplate()
    
    def start_conversation(self) -> str:
        """启动对话，返回开场话术"""
        system_prompt = """你是智能健康管理助手。任务：1)收集用户健康信息 2)信息完整后调用API获取评估 3)完整无损呈现API返回结果。纪律：禁止自己生成医疗建议；禁止删减API返回内容；保留所有格式。"""
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        self.conversation_history.append({"role": "assistant", "content": self.OPENING_MESSAGE})
        return self.OPENING_MESSAGE
    
    def chat(self, user_input: str) -> str:
        """与用户对话，收集信息"""
        self.conversation_history.append({"role": "user", "content": user_input})
        self._parse_user_info(user_input)
        completeness = self._check_info_completeness()
        
        if completeness["is_complete"]:
            self.info_complete = True
            return self._call_api()
        else:
            follow_up = self._generate_follow_up(completeness["missing"])
            self.conversation_history.append({"role": "assistant", "content": follow_up})
            return follow_up
    
    def _parse_user_info(self, user_input: str):
        """解析用户输入，提取结构化信息"""
        if any(kw in user_input for kw in ["岁", "年龄", "男", "女", "姓名", "叫"]):
            self.user_info["basic"]["raw"] = user_input
        if any(kw in user_input for kw in ["病史", "遗传", "家族", "吸烟", "饮酒", "熬夜"]):
            self.user_info["medical"]["raw"] = user_input
        if any(kw in user_input for kw in ["药", "过敏", "孕期", "哺乳", "备孕"]):
            self.user_info["medication"]["raw"] = user_input
        if any(kw in user_input for kw in ["体检", "化验", "报告", "指标", "mmol", "U/L", "g/L"]):
            self.user_info["lab_results"].append(user_input)
    
    def _check_info_completeness(self) -> Dict:
        """检查信息收集是否完整"""
        missing = []
        if not self.user_info["basic"]: missing.append("基础人口学特征")
        if not self.user_info["medical"]: missing.append("健康病史信息")
        if not self.user_info["medication"]: missing.append("用药与特殊状态")
        return {"is_complete": len(missing) == 0, "missing": missing}
    
    def _generate_follow_up(self, missing: List[str]) -> str:
        """根据缺失信息生成追问话术"""
        if not missing: return "感谢您的信息！正在生成健康评估报告..."
        follow_up = "为了生成准确报告，还需了解：\n\n"
        for i, item in enumerate(missing, 1): follow_up += f"{i}. {item}\n"
        return follow_up + "\n请补充以上信息。"
    
    def _call_api(self) -> str:
        """调用后端大模型API获取健康评估"""
        try:
            api_key = _fetch_api_key()
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": self.MODEL, "messages": self.conversation_history, "stream": True, "temperature": 0.7, "max_tokens": 2048}
            response = requests.post(f"{self.BASE_URL}/chat/completions", headers=headers, json=payload, stream=True, timeout=60)
            response.raise_for_status()
            
            full_content = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]
                        if data == '[DONE]': break
                        try:
                            chunk = json.loads(data)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta: full_content += delta['content']
                        except: continue
            
            self.conversation_history.append({"role": "assistant", "content": full_content})
            return full_content
        except requests.exceptions.Timeout:
            return "抱歉，云端健康计算引擎暂时未响应，请稍后再试或重新发送您的数据。"
        except Exception as e:
            return f"抱歉，请求出现异常：{str(e)}。请稍后再试或重新发送您的数据。"
    
    def force_assessment(self) -> str:
        """强制调用API进行评估（即使信息不完整）"""
        return self._call_api()
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history
    
    def get_user_info(self) -> Dict:
        """获取已收集的用户信息"""
        return self.user_info
    
    def get_config(self) -> HealthAssistantConfig:
        """获取配置对象"""
        return self.config
    
    def generate_html_report(
        self,
        patient_data: Dict,
        assessment_result: Dict,
        output_path: str = None
    ) -> str:
        """
        生成HTML健康报告
        
        Args:
            patient_data: 患者基本信息字典
            assessment_result: API返回的评估结果字典
            output_path: 输出文件路径，None则自动生成
        
        Returns:
            HTML报告文件路径
        """
        # 生成报告数据
        report_data = self._build_report_data(patient_data, assessment_result)
        
        # 渲染模板
        html_content = self.template.render(report_data)
        
        # 生成输出路径
        if output_path is None:
            patient_name = patient_data.get("name", "未知")
            date_str = datetime.now().strftime("%Y%m%d")
            skill_dir = Path(__file__).parent.parent.parent
            output_path = skill_dir / f"健康报告_{patient_name}_{date_str}.html"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _build_report_data(self, patient_data: Dict, assessment_result: Dict) -> Dict:
        """构建报告数据字典"""
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        
        # 默认值
        data = {
            # 配置信息
            "SCREENING_URL": self.config.screening_url,
            "SCREENING_NAME": self.config.screening_name,
            "SCREENING_DESCRIPTION": self.config.screening_description,
            "HOTLINE_NUMBER": self.config.hotline_number,
            "REPORT_TITLE": self.config.report_title,
            "REPORT_SUBTITLE": self.config.report_subtitle,
            "POWERED_BY": self.config.powered_by,
            
            # 患者信息
            "PATIENT_NAME": patient_data.get("name", "未知"),
            "PATIENT_AGE": patient_data.get("age", "-"),
            "PATIENT_GENDER": patient_data.get("gender", "未知"),
            "PATIENT_REGION": patient_data.get("region", "未知"),
            "PATIENT_JOB": patient_data.get("job", "未知"),
            "MEDICAL_HISTORY": patient_data.get("medical_history", "无"),
            "FAMILY_HISTORY": patient_data.get("family_history", "无"),
            "LIFESTYLE": patient_data.get("lifestyle", "无"),
            "MEDICATION": patient_data.get("medication", "无"),
            "EXAM_DATE": patient_data.get("exam_date", date_str),
            "EXAM_SOURCE": patient_data.get("exam_source", "用户提供的体检报告"),
            
            # 评估结果
            "ADR_SCORE": str(assessment_result.get("adr_score", "18")),
            "RISK_LEVEL": assessment_result.get("risk_level", "🟡 有潜在风险"),
            "CORE_RISK_FACTORS": assessment_result.get("core_risk_factors", "血脂边缘升高、熬夜"),
            "OVERALL_ASSESSMENT": assessment_result.get("overall_assessment", "暂未见明显器官功能异常"),
            
            # 表格内容（需要HTML格式）
            "LAB_RESULTS_TABLE": assessment_result.get("lab_results_table", self._default_lab_table()),
            "ABNORMAL_INDICATORS_TABLE": assessment_result.get("abnormal_table", self._default_abnormal_table()),
            "DISEASE_RISK_CARDS": assessment_result.get("disease_cards", self._default_disease_cards()),
            "ADVICE_LIST": assessment_result.get("advice_list", self._default_advice_list()),
            "CONCLUSION_TABLE": assessment_result.get("conclusion_table", self._default_conclusion_table()),
            
            # 其他
            "GENERATE_DATE": date_str,
        }
        
        return data
    
    def _default_lab_table(self) -> str:
        """默认体检数据表格"""
        return """<table>
            <tr><th>检查模块</th><th>项目</th><th>检测值</th><th>参考范围</th><th>判定</th></tr>
            <tr><td colspan="5" style="text-align:center;color:#999;">请提供体检报告数据</td></tr>
        </table>"""
    
    def _default_abnormal_table(self) -> str:
        """默认异常指标表格"""
        return """<table>
            <tr><th>指标</th><th>当前结果</th><th>参考判断</th><th>风险值</th><th>风险解读</th></tr>
            <tr><td colspan="5" style="text-align:center;color:#999;">暂无异常指标</td></tr>
        </table>"""
    
    def _default_disease_cards(self) -> str:
        """默认疾病风险卡片"""
        return """<div class="disease-card">
            <div class="disease-item">
                <h4>暂无高风险疾病</h4>
                <span class="risk-level risk-low">✅ 正常</span>
            </div>
        </div>"""
    
    def _default_advice_list(self) -> str:
        """默认建议列表"""
        return """<ul class="advice-list">
            <li><strong>建议：</strong>请根据体检报告结果，参考专业医生建议</li>
        </ul>"""
    
    def _default_conclusion_table(self) -> str:
        """默认结论表格"""
        return """<table>
            <tr><th style="width:30%">评估类别</th><th>结论</th></tr>
            <tr><td>综合风险等级</td><td>🟡 待评估</td></tr>
        </table>"""
    
    def open_report_in_browser(self, report_path: str) -> bool:
        """在浏览器中打开报告"""
        try:
            webbrowser.open(f"file:///{report_path.replace(chr(92), '/')}")
            return True
        except Exception:
            return False


# 便捷函数接口
def start_health_assessment() -> str:
    """启动健康评估对话"""
    assistant = HealthAssistant()
    return assistant.start_conversation()


def continue_health_chat(assistant: HealthAssistant, user_input: str) -> str:
    """继续健康评估对话"""
    return assistant.chat(user_input)


def generate_report(
    patient_data: Dict,
    assessment_result: Dict,
    output_path: str = None
) -> str:
    """生成HTML健康报告"""
    assistant = HealthAssistant()
    return assistant.generate_html_report(patient_data, assessment_result, output_path)


# 示例用法
if __name__ == "__main__":
    # 测试配置加载
    config = HealthAssistantConfig()
    print(f"筛查链接: {config.screening_url}")
    print(f"联系电话: {config.hotline_number}")
    print(f"报告标题: {config.report_title}")
    
    # 测试报告生成
    patient = {
        "name": "张敏",
        "age": "32",
        "gender": "女",
        "region": "北京",
        "job": "工程师",
        "medical_history": "无",
        "family_history": "无",
        "lifestyle": "熬夜",
        "medication": "无"
    }
    
    assessment = {
        "adr_score": "18",
        "risk_level": "🟡 有潜在风险",
        "core_risk_factors": "总胆固醇边缘升高、甘油三酯边缘升高",
        "overall_assessment": "暂未见明显器官功能异常，但已出现早期代谢风险信号"
    }
    
    assistant = HealthAssistant()
    report_path = assistant.generate_html_report(patient, assessment)
    print(f"\n报告已生成: {report_path}")
