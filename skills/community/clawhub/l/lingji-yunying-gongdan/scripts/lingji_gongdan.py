#!/usr/bin/env python3
"""
灵畿运营工单分析脚本
"""
import sys
import pandas as pd
import re
from pathlib import Path

def parse_duration(s):
    """解析处理时长，返回分钟数"""
    if pd.isna(s):
        return None
    s = str(s)
    days = re.search(r'(\d+)天', s)
    hours = re.search(r'(\d+)小时', s)
    minutes = re.search(r'(\d+)分', s)
    seconds = re.search(r'(\d+)秒', s)
    total_minutes = 0
    if days: total_minutes += int(days.group(1)) * 24 * 60
    if hours: total_minutes += int(hours.group(1)) * 60
    if minutes: total_minutes += int(minutes.group(1))
    if seconds: total_minutes += int(seconds.group(1)) / 60
    return total_minutes

def cmd_stats(df):
    """整体统计"""
    print("\n" + "="*50)
    print("📊 整体概况")
    print("="*50)
    print(f"工单总量：{len(df)}")
    print("\n📋 工单类型分布：")
    for t, c in df['工单类型'].value_counts().items():
        print(f"  {t}: {c} ({c/len(df)*100:.1f}%)")
    
    print("\n📋 工单状态分布：")
    for s, c in df['工单状态'].value_counts().items():
        print(f"  {s}: {c} ({c/len(df)*100:.1f}%)")
    
    print("\n📋 归属域分布：")
    for d, c in df['归属域'].value_counts().items():
        print(f"  {d}: {c} ({c/len(df)*100:.1f}%)")
    
    print("\n📋 满意度分布：")
    for sat, c in df['满意度选项'].value_counts().items():
        print(f"  {sat}: {c}")

def cmd_handlers(df):
    """处理人统计"""
    print("\n" + "="*50)
    print("👥 支撑人员分析（按处理量排名）")
    print("="*50)
    
    top_handlers = df['当前处理人'].value_counts().head(15).index.tolist()
    
    print(f"{'处理人':<10} {'工单数':>6} {'已完成':>6} {'待确认':>6} {'非常满意':>8} {'平均满意度':>10} {'平均处理时长':>12}")
    print("-"*70)
    
    for handler in top_handlers:
        h_df = df[df['当前处理人'] == handler]
        total = len(h_df)
        completed = (h_df['工单状态'] == '红军已完成').sum()
        pending = (h_df['工单状态'] == '待用户确认').sum()
        very_sat = (h_df['满意度选项'] == '非常满意').sum()
        
        # 只计算有效满意度（>0）
        valid_sat = h_df[h_df['满意度分值'] > 0]['满意度分值']
        avg_sat = valid_sat.mean() if len(valid_sat) > 0 else 0
        
        h_df_copy = h_df.copy()
        h_df_copy['时长_分钟'] = h_df_copy['工单处理时长'].apply(parse_duration)
        avg_time = h_df_copy['时长_分钟'].mean()
        
        print(f"{handler:<10} {total:>6} {completed:>6} {pending:>6} {very_sat:>8} {avg_sat:>10.1f} {avg_time:>10.0f}分钟")

def cmd_timing(df):
    """时效分析"""
    print("\n" + "="*50)
    print("⏱️ 时效性分析")
    print("="*50)
    
    df_copy = df.copy()
    df_copy['处理时长_分钟'] = df_copy['工单处理时长'].apply(parse_duration)
    
    valid_times = df_copy['处理时长_分钟'].dropna()
    print(f"平均处理时长: {valid_times.mean():.0f} 分钟")
    print(f"中位数处理时长: {valid_times.median():.0f} 分钟")
    print(f"最短处理时长: {valid_times.min():.0f} 分钟")
    print(f"最长处理时长: {valid_times.max():.0f} 分钟")
    print(f"90分位处理时长: {valid_times.quantile(0.9):.0f} 分钟")
    
    print("\n📋 响应超时状态：")
    for status, count in df['响应超时状态'].value_counts().items():
        print(f"  {status}: {count}")
    
    # 超时工单明细
    timeout_df = df[df['响应超时状态'] == '已超时']
    if len(timeout_df) > 0:
        print(f"\n⚠️ 超时工单明细（共{len(timeout_df)}条）：")
        for _, row in timeout_df.head(10).iterrows():
            print(f"  - {row['工单单号']} | {row['当前处理人']} | 超期: {row['响应超期信息']}")

def cmd_satisfaction(df):
    """满意度分析"""
    print("\n" + "="*50)
    print("😊 满意度分析")
    print("="*50)
    
    # 有效满意度
    valid_df = df[df['满意度分值'] > 0]
    print(f"有效满意度评价: {len(valid_df)}/{len(df)} ({len(valid_df)/len(df)*100:.1f}%)")
    
    print("\n📋 满意度分布：")
    for opt, cnt in df['满意度选项'].value_counts().items():
        pct = cnt / len(df) * 100
        print(f"  {opt}: {cnt} ({pct:.1f}%)")
    
    print(f"\n整体平均满意度分值: {df['满意度分值'].mean():.2f}")
    print(f"有效评价平均分: {valid_df['满意度分值'].mean():.2f}")
    
    # 处理人满意度排名
    print("\n📋 支撑人员满意度排名（处理量>5）：")
    handler_sat = df.groupby('当前处理人').agg({
        '满意度分值': lambda x: x[x > 0].mean(),
        '当前处理人': 'count'
    }).round(2)
    handler_sat.columns = ['平均分', '处理量']
    handler_sat = handler_sat[handler_sat['处理量'] > 5].sort_values('平均分', ascending=False)
    
    for handler, row in handler_sat.head(10).iterrows():
        print(f"  {handler}: {row['平均分']:.1f}分 ({row['处理量']:.0f}件)")

def cmd_hot(df):
    """热点问题分析"""
    import re
    from collections import Counter
    
    print("\n" + "="*50)
    print("🔥 热点问题分析")
    print("="*50)
    
    # 细粒度问题分类
    def classify_issue(desc):
        if pd.isna(desc):
            return []
        desc = str(desc)
        issues = []
        
        # 权限问题
        if '权限' in desc or '看不了' in desc or '看不到' in desc or '无法查看' in desc:
            issues.append('权限问题')
        
        # 项目查询/找不到
        if '查询不到' in desc or '看不到项目' in desc or '找不到项目' in desc or '搜索不到' in desc:
            issues.append('项目查询不到')
        
        # 立项/挂载问题
        if '立项' in desc or '挂载' in desc or '关联需求' in desc:
            issues.append('立项/需求关联')
        
        # 系统报错
        if '报错' in desc or '异常' in desc or '失败' in desc:
            if '上传失败' in desc or '导入失败' in desc:
                issues.append('上传/导入失败')
            elif '服务器异常' in desc or '系统异常' in desc:
                issues.append('服务器异常')
            else:
                issues.append('系统报错')
        
        # 流程审批
        if '审批' in desc or '流程' in desc:
            issues.append('流程审批')
        
        # 数据问题
        if '数据' in desc or '金额不对' in desc or '金额有误' in desc:
            issues.append('数据问题')
        
        # 预算问题
        if '预算' in desc:
            issues.append('预算问题')
        
        # 登录问题
        if '登录' in desc or '登陆' in desc:
            issues.append('登录问题')
        
        # 证书问题
        if '证书' in desc:
            issues.append('证书问题')
        
        # 删除问题
        if '删除' in desc:
            issues.append('删除问题')
        
        # 修改/编辑问题
        if '修改' in desc or '编辑' in desc:
            if '无法编辑' in desc or '编辑不了' in desc:
                issues.append('编辑保存问题')
        
        # 建议/优化
        if '建议' in desc or '优化' in desc:
            issues.append('建议/优化需求')
        
        # 需求管理
        if '需求' in desc:
            issues.append('需求管理')
        
        # 成果问题
        if '成果' in desc:
            issues.append('成果管理')
        
        # 研发计划
        if '研发计划' in desc:
            issues.append('研发计划')
        
        # 制品/仓库
        if '制品' in desc or '仓库' in desc:
            issues.append('制品/仓库')
        
        return issues if issues else ['其他问题']
    
    # 统计问题类型
    all_issues = []
    for desc in df['工单内容描述']:
        all_issues.extend(classify_issue(desc))
    
    issue_counts = Counter(all_issues)
    
    print("\n📋 细分问题类型TOP20：")
    for issue, cnt in issue_counts.most_common(20):
        pct = cnt / len(df) * 100
        print(f"  {issue}: {cnt} ({pct:.1f}%)")
    
    # 高频模块
    print("\n📋 高频模块TOP10：")
    for module, cnt in df['模块'].value_counts().head(10).items():
        print(f"  {module}: {cnt}")
    
    # 高频菜单
    print("\n📋 高频菜单TOP10：")
    for menu, cnt in df['菜单'].value_counts().head(10).items():
        print(f"  {menu}: {cnt}")
    
    print("\n📋 处理工作组TOP10：")
    for group, cnt in df['处理工作组'].value_counts().head(10).items():
        print(f"  {group}: {cnt}")

def cmd_full_report(df):
    """完整报告"""
    print("\n" + "="*60)
    print("       灵畿科研平台工单运营分析报告")
    print("="*60)
    
    cmd_stats(df)
    cmd_handlers(df)
    cmd_timing(df)
    cmd_satisfaction(df)
    cmd_hot(df)
    
    print("\n" + "="*60)
    print("                    报告生成完成")
    print("="*60)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 lingji_gongdan.py <command> <excel_file>")
        print("Commands: stats, handlers, timing, satisfaction, hot, report")
        sys.exit(1)
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    
    print(f"Loading data from: {file_path}")
    df = pd.read_excel(file_path)
    print(f"Loaded {len(df)} records\n")
    
    if command == "stats":
        cmd_stats(df)
    elif command == "handlers":
        cmd_handlers(df)
    elif command == "timing":
        cmd_timing(df)
    elif command == "satisfaction":
        cmd_satisfaction(df)
    elif command == "hot":
        cmd_hot(df)
    elif command == "report":
        cmd_full_report(df)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
