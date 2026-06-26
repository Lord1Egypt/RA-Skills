#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA工单自动分析处理脚本
自动分析新工单内容，检查四项必填信息，根据规则自动处理
"""

import os
import sys
import json
import re
import time
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import logging

# 添加父目录到路径，以便导入utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  警告：Playwright未安装，请运行：pip install playwright")
    print("然后运行：python3 -m playwright install chromium")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '..', 'logs', 'jira_analyze.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JIRAAutoAnalyzer:
    """JIRA工单自动分析处理器"""
    
    def __init__(self, config_path: str = None, dry_run: bool = False):
        """初始化分析器
        
        Args:
            config_path: 配置文件路径
            dry_run: 模拟运行模式（不实际修改）
        """
        self.dry_run = dry_run
        self.config = self._load_config(config_path)
        self.rules = self.config.get('rules', [])
        self.jira_config = self.config.get('config', {})
        
        # JIRA登录凭证
        self.jira_credentials = {
            'username': self.jira_config.get('username', 'liuwei1'),
            'password': self.jira_config.get('password', 'Lw@123456')
        }
        
        # 浏览器实例
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # 统计信息
        self.stats = {
            'total_issues': 0,
            'new_issues': 0,
            'valid_issues': 0,
            'rejected_issues': 0,
            'assigned_issues': 0,
            'processed_issues': 0
        }
        
        # 必填信息检查项
        self.required_fields = {
            '环境': ['星舰', '飞船', '云'],
            '通道类型': ['web连接器', 'rpa', '乐企'],
            '项目版本号': r'(\d+\.\d+\.\d+|v\d+|版本\d+)',
            '相关日志': ['日志', 'log', 'trace', 'error', 'stack']
        }
        
        logger.info(f"初始化JIRA自动分析器，模式：{'模拟运行' if dry_run else '实际执行'}")
        
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            # 默认配置文件路径
            config_path = os.path.join(
                os.path.dirname(__file__), '..', 'config', 'config.json'
            )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"成功加载配置文件：{config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"配置文件不存在：{config_path}")
            # 返回默认配置
            return self._get_default_config()
        except json.JSONDecodeError:
            logger.error(f"配置文件格式错误：{config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "rules": [
                {
                    "rule_name": "认证相关工单",
                    "keywords": ["认证", "勾选", "授权", "权限", "token", "登录", "Auth"],
                    "assignee": "张献文",
                    "jira_username": "zhangxianwen",
                    "reply_message": "请献文协助处理此工单"
                },
                {
                    "rule_name": "乐企相关工单",
                    "keywords": ["乐企", "leqi", "LEQI"],
                    "assignee": "付强",
                    "jira_username": "fuqiang",
                    "reply_message": "请付强协助处理此工单"
                },
                {
                    "rule_name": "综服通道相关工单",
                    "keywords": ["综服", "通道", "银行", "工行", "中行", "农行", "建行", "招行"],
                    "assignee": "魏旭峰",
                    "jira_username": "weixufeng",
                    "reply_message": "请旭峰协助处理此工单"
                },
                {
                    "rule_name": "其他工单",
                    "keywords": [],
                    "assignee": "刘巍",
                    "jira_username": "liuwei1",
                    "reply_message": "收到，我会及时处理，请稍后"
                }
            ],
            "config": {
                "jira_url": "http://jira.51baiwang.com",
                "filter_id": "13123",
                "username": "liuwei1",
                "password": "Lw@123456",
                "rejection_message": "请提供相关环境、通道类型、版本号及日志信息",
                "check_new_only": True  # 只检查新工单
            }
        }
    
    def _init_browser(self):
        """初始化浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright未安装，无法运行浏览器自动化")
        
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=True,  # 无头模式
            args=['--disable-blink-features=AutomationControlled']  # 避免被检测为自动化
        )
        
        # 创建上下文
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        self.page = self.context.new_page()
        logger.info("浏览器初始化完成")
    
    def _login_jira(self) -> bool:
        """登录JIRA系统"""
        try:
            jira_url = self.jira_config.get('jira_url', 'http://jira.51baiwang.com')
            logger.info(f"正在访问JIRA: {jira_url}")
            
            self.page.goto(jira_url, wait_until='networkidle')
            time.sleep(2)
            
            # 检查是否已经登录
            if self.page.locator('#header-details-user-fullname').count() > 0:
                logger.info("检测到已登录状态")
                return True
            
            # 执行登录
            logger.info("执行登录操作...")
            
            # 输入用户名
            username_input = self.page.locator('#login-form-username')
            if username_input.count() > 0:
                username_input.fill(self.jira_credentials['username'])
                time.sleep(0.5)
            
            # 输入密码
            password_input = self.page.locator('#login-form-password')
            if password_input.count() > 0:
                password_input.fill(self.jira_credentials['password'])
                time.sleep(0.5)
            
            # 点击登录按钮
            submit_button = self.page.locator('#login-form-submit')
            if submit_button.count() > 0:
                submit_button.click()
                time.sleep(3)
            
            # 验证登录是否成功
            if self.page.locator('#header-details-user-fullname').count() > 0:
                logger.info("JIRA登录成功")
                return True
            else:
                logger.error("JIRA登录失败")
                return False
                
        except Exception as e:
            logger.error(f"登录JIRA时发生错误: {str(e)}")
            return False
    
    def _navigate_to_filter(self) -> bool:
        """导航到指定的filter页面"""
        try:
            filter_id = self.jira_config.get('filter_id', '13123')
            filter_url = f"{self.jira_config.get('jira_url')}/issues/?filter={filter_id}"
            
            logger.info(f"正在访问filter页面: {filter_url}")
            self.page.goto(filter_url, wait_until='networkidle')
            time.sleep(5)  # 等待表格加载
            
            # 检查是否成功加载
            if self.page.locator('tr.issuerow').count() > 0:
                logger.info(f"成功加载filter页面，找到工单表格")
                return True
            else:
                logger.warning("未找到工单表格，可能需要等待更长时间或检查页面结构")
                # 尝试等待更长时间
                time.sleep(10)
                if self.page.locator('tr.issuerow').count() > 0:
                    logger.info("重新检查后找到工单表格")
                    return True
                return False
                
        except Exception as e:
            logger.error(f"导航到filter页面时发生错误: {str(e)}")
            return False
    
    def _extract_issues(self) -> List[Dict]:
        """从页面提取工单信息"""
        issues = []
        
        try:
            # 查找所有工单行
            issue_rows = self.page.locator('tr.issuerow')
            count = issue_rows.count()
            logger.info(f"找到 {count} 个工单行")
            
            for i in range(min(count, 50)):  # 限制最多处理50个
                try:
                    row = issue_rows.nth(i)
                    
                    # 提取各列数据（根据已知的列索引）
                    cells = row.locator('td')
                    
                    # 状态（第0列）
                    status = cells.nth(0).inner_text().strip() if cells.nth(0).count() > 0 else ""
                    
                    # 工单号（第1列）
                    issue_key_elem = cells.nth(1).locator('a')
                    issue_key = issue_key_elem.inner_text().strip() if issue_key_elem.count() > 0 else ""
                    issue_link = issue_key_elem.get_attribute('href') if issue_key_elem.count() > 0 else ""
                    
                    # 概要（第2列）
                    summary = cells.nth(2).inner_text().strip() if cells.nth(2).count() > 0 else ""
                    
                    # 经办人（第8列）
                    assignee = cells.nth(8).inner_text().strip() if cells.nth(8).count() > 0 else ""
                    
                    # 产品模块（第12列）
                    product = cells.nth(12).inner_text().strip() if cells.nth(12).count() > 0 else ""
                    
                    # 创建日期（第3列）
                    created_date = cells.nth(3).inner_text().strip() if cells.nth(3).count() > 0 else ""
                    
                    # 只处理新工单（状态为"新建"）
                    check_new_only = self.jira_config.get('check_new_only', True)
                    if check_new_only and status != "新建":
                        continue
                    
                    issue = {
                        'row_index': i,
                        'status': status,
                        'issue_key': issue_key,
                        'issue_link': issue_link,
                        'summary': summary,
                        'assignee': assignee,
                        'product': product,
                        'created_date': created_date,
                        'is_valid': False,
                        'missing_fields': [],
                        'suggested_assignee': None,
                        'suggested_reply': None,
                        'rule_matched': None,
                        'needs_action': False
                    }
                    
                    issues.append(issue)
                    
                except Exception as e:
                    logger.warning(f"提取第 {i} 行工单时出错: {str(e)}")
                    continue
            
            self.stats['total_issues'] = len(issues)
            logger.info(f"成功提取 {len(issues)} 个工单")
            
        except Exception as e:
            logger.error(f"提取工单信息时发生错误: {str(e)}")
        
        return issues
    
    def _analyze_issue_content(self, issue: Dict) -> Dict:
        """分析工单内容，检查四项必填信息"""
        summary = issue.get('summary', '')
        description = self._get_issue_description(issue)
        full_text = f"{summary} {description}".lower()
        
        missing_fields = []
        
        # 检查环境信息
        env_found = False
        for env in self.required_fields['环境']:
            if env in full_text:
                env_found = True
                break
        if not env_found:
            missing_fields.append('环境（星舰、飞船、云）')
        
        # 检查通道类型
        channel_found = False
        for channel in self.required_fields['通道类型']:
            if channel in full_text:
                channel_found = True
                break
        if not channel_found:
            missing_fields.append('通道类型（web连接器、rpa、乐企）')
        
        # 检查项目版本号（云工单除外）
        version_found = False
        if '云' in full_text:
            # 云工单不需要版本号
            version_found = True
        else:
            version_pattern = self.required_fields['项目版本号']
            if re.search(version_pattern, full_text):
                version_found = True
        if not version_found:
            missing_fields.append('项目相关服务模块版本号')
        
        # 检查相关日志
        log_found = False
        for log_keyword in self.required_fields['相关日志']:
            if log_keyword in full_text:
                log_found = True
                break
        if not log_found:
            missing_fields.append('相关日志信息')
        
        issue['missing_fields'] = missing_fields
        issue['is_valid'] = len(missing_fields) == 0
        
        if issue['is_valid']:
            issue['needs_action'] = True
            logger.info(f"工单 {issue.get('issue_key')} 验证通过")
        else:
            issue['needs_action'] = True  # 需要打回
            logger.info(f"工单 {issue.get('issue_key')} 缺少字段: {missing_fields}")
        
        return issue
    
    def _get_issue_description(self, issue: Dict) -> str:
        """获取工单详细描述"""
        try:
            issue_key = issue.get('issue_key')
            if not issue_key:
                return ""
            
            # 打开工单详情页
            issue_url = f"{self.jira_config.get('jira_url')}/browse/{issue_key}"
            self.page.goto(issue_url, wait_until='networkidle')
            time.sleep(2)
            
            # 提取描述信息
            description = ""
            
            # 尝试多个可能的描述元素
            selectors = [
                '#description-val',
                '.description',
                '.issue-body-content',
                '.user-content-block'
            ]
            
            for selector in selectors:
                desc_elem = self.page.locator(selector)
                if desc_elem.count() > 0:
                    description = desc_elem.inner_text()
                    break
            
            # 返回filter页面
            filter_id = self.jira_config.get('filter_id', '13123')
            filter_url = f"{self.jira_config.get('jira_url')}/issues/?filter={filter_id}"
            self.page.goto(filter_url, wait_until='networkidle')
            time.sleep(3)
            
            return description.lower()
            
        except Exception as e:
            logger.warning(f"获取工单 {issue.get('issue_key', '未知')} 描述时出错: {str(e)}")
            return ""
    
    def _determine_assignment(self, issue: Dict) -> Dict:
        """根据工单内容确定分配规则"""
        if not issue.get('is_valid'):
            return issue
        
        summary = issue.get('summary', '').lower()
        best_match = None
        best_score = 0
        
        # 应用所有规则进行匹配
        for rule in self.rules:
            keywords = rule.get('keywords', [])
            match_score = self._calculate_match_score(summary, keywords)
            
            if match_score > best_score:
                best_score = match_score
                best_match = rule
        
        # 如果匹配到规则，使用该规则；否则使用"其他工单"规则
        if best_match and best_score > 0:
            issue['rule_matched'] = best_match.get('rule_name')
            issue['suggested_assignee'] = best_match.get('assignee')
            issue['suggested_jira_username'] = best_match.get('jira_username')
            issue['suggested_reply'] = best_match.get('reply_message')
        else:
            # 使用"其他工单"规则
            other_rule = next((r for r in self.rules if r['rule_name'] == '其他工单'), None)
            if other_rule:
                issue['rule_matched'] = other_rule.get('rule_name')
                issue['suggested_assignee'] = other_rule.get('assignee')
                issue['suggested_jira_username'] = other_rule.get('jira_username')
                issue['suggested_reply'] = other_rule.get('reply_message')
        
        return issue
    
    def _calculate_match_score(self, text: str, keywords: List[str]) -> float:
        """计算文本与关键词的匹配分数"""
        if not text or not keywords:
            return 0.0
        
        text_lower = text.lower()
        matches = 0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in text_lower:
                matches += 1
                # 如果关键词较长，给予更高权重
                weight = min(len(keyword) / 10, 1.0)
                matches += weight
        
        # 计算分数：匹配的关键词数量 / 总关键词数量
        score = matches / len(keywords) if keywords else 0
        return min(score, 1.0)  # 确保不超过1.0
    
    def _reject_issue(self, issue: Dict) -> bool:
        """打回工单给联系人"""
        if self.dry_run:
            logger.info(f"[模拟] 将工单 {issue['issue_key']} 打回给联系人")
            return True
        
        try:
            issue_key = issue.get('issue_key')
            if not issue_key:
                logger.error("工单号为空，无法打回")
                return False
            
            # 打开工单详情页
            issue_url = f"{self.jira_config.get('jira_url')}/browse/{issue_key}"
            self.page.goto(issue_url, wait_until='networkidle')
            time.sleep(2)
            
            # 添加评论打回
            rejection_message = self.jira_config.get('rejection_message', '请提供相关环境、通道类型、版本号及日志信息')
            comment = f"{rejection_message}\n\n缺少的信息：{', '.join(issue['missing_fields'])}"
            
            # 点击"评论"按钮
            comment_button = self.page.locator('#comment-issue')
            if comment_button.count() > 0:
                comment_button.click()
                time.sleep(1)
            
            # 输入评论内容
            comment_textarea = self.page.locator('#comment')
            if comment_textarea.count() > 0:
                comment_textarea.fill(comment)
                time.sleep(1)
            
            # 提交评论
            submit_button = self.page.locator('#issue-comment-add-submit')
            if submit_button.count() > 0:
                submit_button.click()
                time.sleep(2)
            
            logger.info(f"成功打回工单 {issue_key}")
            return True
            
        except Exception as e:
            logger.error(f"打回工单 {issue.get('issue_key', '未知')} 时发生错误: {str(e)}")
            return False
    
    def _assign_and_reply(self, issue: Dict) -> bool:
        """分配工单并回复"""
        if self.dry_run:
            logger.info(f"[模拟] 将工单 {issue['issue_key']} 分配给 {issue['suggested_assignee']} 并回复")
            return True
        
        try:
            issue_key = issue.get('issue_key')
            if not issue_key:
                logger.error("工单号为空，无法分配")
                return False
            
            # 打开工单详情页
            issue_url = f"{self.jira_config.get('jira_url')}/browse/{issue_key}"
            self.page.goto(issue_url, wait_until='networkidle')
            time.sleep(2)
            
            # 1. 分配工单
            # 点击"编辑"按钮
            edit_button = self.page.locator('#edit-issue')
            if edit_button.count() > 0:
                edit_button.click()
                time.sleep(2)
            
            # 修改经办人字段
            assignee_field = self.page.locator('#assignee-field')
            if assignee_field.count() > 0:
                assignee_field.fill(issue['suggested_jira_username'])
                time.sleep(1)
                
                # 提交更改
                submit_button = self.page.locator('#edit-issue-submit')
                if submit_button.count() > 0:
                    submit_button.click()
                    time.sleep(3)
            
            # 2. 添加回复评论
            reply_message = issue.get('suggested_reply', '')
            if reply_message:
                # 点击"评论"按钮
                comment_button = self.page.locator('#comment-issue')
                if comment_button.count() > 0:
                    comment_button.click()
                    time.sleep(1)
                
                # 输入评论内容
                comment_textarea = self.page.locator('#comment')
                if comment_textarea.count() > 0:
                    comment_textarea.fill(reply_message)
                    time.sleep(1)
                
                # 提交评论
                submit_button = self.page.locator('#issue-comment-add-submit')
                if submit_button.count() > 0:
                    submit_button.click()
                    time.sleep(2)
            
            logger.info(f"成功分配工单 {issue_key} 给 {issue['suggested_assignee']} 并回复")
            return True
            
        except Exception as e:
            logger.error(f"分配工单 {issue.get('issue_key', '未知')} 时发生错误: {str(e)}")
            return False
    
    def _log_operation(self, issue: Dict, operation: str, success: bool):
        """记录操作日志"""
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'operation_log.md')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "✅ 成功" if success else "❌ 失败"
        
        log_entry = f"""
## {timestamp} - {issue.get('issue_key', '未知工单')} - {operation}

- **工单**: {issue.get('issue_key')}
- **概要**: {issue.get('summary')}
- **状态**: {issue.get('status')}
- **操作**: {operation}
- **详情**: 
  - 是否有效: {'是' if issue.get('is_valid') else '否'}
  - 缺少字段: {', '.join(issue.get('missing_fields', []))}
  - 匹配规则: {issue.get('rule_matched', '无')}
  - 建议经办人: {issue.get('suggested_assignee', '无')}
- **操作结果**: {status}
- **操作模式**: {'模拟运行' if self.dry_run else '实际执行'}

---
"""
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            logger.error(f"写入日志文件失败: {str(e)}")
    
    def run(self):
        """运行自动分析处理流程"""
        logger.info("🚀 开始JIRA工单自动分析处理流程")
        
        try:
            # 1. 初始化浏览器
            self._init_browser()
            
            # 2. 登录JIRA
            if not self._login_jira():
                logger.error("登录失败，终止流程")
                return
            
            # 3. 导航到filter页面
            if not self._navigate_to_filter():
                logger.error("访问filter页面失败，终止流程")
                return
            
            # 4. 提取工单
            issues = self._extract_issues()
            if not issues:
                logger.warning("未提取到任何新工单")
                return
            
            self.stats['new_issues'] = len(issues)
            
            # 5. 分析工单内容
            logger.info("🔍 开始分析工单内容...")
            for i, issue in enumerate(issues):
                issues[i] = self._analyze_issue_content(issue)
                if issues[i]['is_valid']:
                    self.stats['valid_issues'] += 1
                    # 确定分配规则
                    issues[i] = self._determine_assignment(issues[i])
                else:
                    self.stats['rejected_issues'] += 1
            
            # 6. 显示分析结果
            self._display_analysis(issues)
            
            # 7. 执行处理
            if not self.dry_run and (self.stats['valid_issues'] > 0 or self.stats['rejected_issues'] > 0):
                total_actions = self.stats['valid_issues'] + self.stats['rejected_issues']
                confirm = input(f"\n⚠️  确认要处理 {total_actions} 个工单吗？(y/N): ")
                if confirm.lower() != 'y':
                    logger.info("用户取消操作")
                    return
            
            logger.info("🔄 开始执行处理...")
            for issue in issues:
                if not issue.get('needs_action'):
                    continue
                
                if issue.get('is_valid'):
                    # 有效工单：分配并回复
                    success = self._assign_and_reply(issue)
                    if success:
                        self.stats['assigned_issues'] += 1
                        self.stats['processed_issues'] += 1
                    self._log_operation(issue, "分配并回复", success)
                else:
                    # 无效工单：打回
                    success = self._reject_issue(issue)
                    if success:
                        self.stats['processed_issues'] += 1
                    self._log_operation(issue, "打回工单", success)
            
            # 8. 显示最终统计
            self._display_final_stats()
            
        except Exception as e:
            logger.error(f"运行自动分析处理流程时发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 清理资源
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            logger.info("浏览器资源已清理")
    
    def _display_analysis(self, issues: List[Dict]):
        """显示分析结果"""
        print("\n" + "="*100)
        print("📊 JIRA工单分析处理结果")
        print("="*100)
        
        valid_issues = [i for i in issues if i.get('is_valid')]
        rejected_issues = [i for i in issues if not i.get('is_valid')]
        
        print(f"\n📋 发现 {self.stats['total_issues']} 个工单")
        print(f"   - 新工单: {self.stats['new_issues']}")
        print(f"   - 有效工单: {len(valid_issues)}")
        print(f"   - 需打回工单: {len(rejected_issues)}")
        
        if rejected_issues:
            print("\n❌ 需要打回的工单:")
            print("-"*100)
            for issue in rejected_issues:
                print(f"\n{issue['issue_key']} - {issue['summary'][:50]}...")
                print(f"  缺少信息: {', '.join(issue['missing_fields'])}")
        
        if valid_issues:
            print("\n✅ 有效的工单:")
            print("-"*100)
            for issue in valid_issues:
                print(f"\n{issue['issue_key']} - {issue['summary'][:50]}...")
                print(f"  匹配规则: {issue.get('rule_matched', '其他工单')}")
                print(f"  建议分配: {issue.get('suggested_assignee', '刘巍')}")
                print(f"  回复内容: {issue.get('suggested_reply', '收到，我会及时处理，请稍后')}")
        
        # 按规则统计
        if valid_issues:
            rule_stats = {}
            for issue in valid_issues:
                rule = issue.get('rule_matched', '其他工单')
                rule_stats[rule] = rule_stats.get(rule, 0) + 1
            
            print("\n🎯 按规则分配统计:")
            for rule, count in rule_stats.items():
                print(f"- {rule}: {count} 个工单")
    
    def _display_final_stats(self):
        """显示最终统计信息"""
        print("\n" + "="*100)
        print("🎯 处理完成")
        print("="*100)
        
        print(f"\n📊 最终统计:")
        print(f"- 总工单数: {self.stats['total_issues']}")
        print(f"- 新工单数: {self.stats['new_issues']}")
        print(f"- 有效工单: {self.stats['valid_issues']}")
        print(f"- 打回工单: {self.stats['rejected_issues']}")
        print(f"- 分配工单: {self.stats['assigned_issues']}")
        print(f"- 处理工单: {self.stats['processed_issues']}")
        
        if self.dry_run:
            print("\n💡 注意：本次为模拟运行模式，未实际修改JIRA数据")
        
        print(f"\n⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*100)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='JIRA工单自动分析处理工具')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际修改数据')
    parser.add_argument('--config', type=str, help='配置文件路径')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not PLAYWRIGHT_AVAILABLE:
        print("错误：请先安装Playwright")
        print("运行: pip install playwright")
        print("然后运行: python3 -m playwright install chromium")
        sys.exit(1)
    
    # 创建分析器
    analyzer = JIRAAutoAnalyzer(
        config_path=args.config,
        dry_run=args.dry_run
    )
    
    # 运行分析处理流程
    analyzer.run()

if __name__ == '__main__':
    main()