# Pharmaceutical System Bidding Information Collection Skill

## Overview
This skill automates the collection and analysis of pharmaceutical system related bidding information from provincial procurement websites. It performs verification, filtering, and evaluation to identify promising bidding opportunities for sales teams.

## Workflow

### 1. Information Collection
- **Source**: Search provincial procurement websites using targeted keywords
- **Query**: "药学系统" (pharmaceutical system) related bidding information
- **Output**: Collect bidding information with source URLs

### 2. Verification & Filtering
For each collected item, verify all criteria:
- ✅ Product is a pharmaceutical system
- ✅ Deadline for obtaining bidding documents > 2 days
- ❌ Skip if any criteria fail

### 3. Secondary Research (if needed)
- When source URLs lack sufficient information
- Use search engines to gather additional details
- Apply same verification criteria

### 4. Data Recording
Record key information in WeChat Work smart table:
- 购标截止日期 (Bid document deadline)
- 开标日期 (Bid opening date)
- 招标单位 (Bidding unit)
- 项目名称 (Project name)
- 预算金额 (Budget amount)
- 涉及产品范围 (Product scope)
- 对应负责销售 (Responsible sales person)

### 5. Evaluation & Bidding Suggestions
**If bidding documents available:**
- Analyze bidding qualifications
- Review technical parameters
- Assess project budget
- Evaluate bid opening time
- Provide bidding recommendations

**If no bidding documents available:**
- Evaluate bid opening time
- Assess project budget
- Analyze product requirements
- Provide bidding recommendations

### 6. Project Classification
Mark as "可参与项目" (Participate) if meeting ANY criteria:
- 开标时间 - 当日日期 > 10天 AND 购标截止日期 - 当日日期 > 2天
- 项目预算金额 > 100万元
- 招标单位为三级医院或县人民医院

## Scheduled Execution
- **Time**: Daily at 8:30 AM
- **Action**: Automatically collect and populate WeChat Work smart table

## Required Tools
- Web search functionality
- Web scraping capabilities
- Data verification logic
- WeChat Work API integration
- Scheduling system

## Configuration
- Target procurement websites to monitor
- WeChat Work smart table integration details
- Sales team assignment rules
- Budget thresholds
- Hospital classification criteria