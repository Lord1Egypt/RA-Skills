---
name: internal-medicine-pmph-10edition
description: >
  432 项基于人民卫生出版社《内科学》第10版（五年制本科临床医学专业第十轮规划教材）的核心临床技能集合。
  涵盖心血管、呼吸、消化、内分泌与代谢、肾脏、血液、风湿免疫、感染、中毒与理化损伤及肿瘤综合等亚专业领域。
  当用户输入与内科学相关的临床问题（症状、疾病、检验异常、治疗方案、药物调整等）时，自动匹配并调用相应的技能模块。
  每个技能聚焦于疾病诊断标准、风险评估、治疗策略、实验室与影像解读、急症处理及慢病管理等关键临床场景。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://docs.openclaw.ai/clawhub/skill-format
    emoji: "🩺"
    requires:
      - name: node
        version: ">=18.0.0"
    install:
      steps:
        - name: install-deps
          run: npm install
      cwd: .
    envVars:
      - name: SKILL_INDEX_PATH
        description: Path to skills index JSON file
        default: config/skills-index.json
    

categories:
  - name: 心血管疾病
    count: 97
  - name: 内分泌与代谢疾病
    count: 64
  - name: 呼吸系统疾病
    count: 60
  - name: 血液系统疾病
    count: 55
  - name: 消化系统疾病
    count: 50
  - name: 肾脏疾病
    count: 35
  - name: 中毒与理化损伤
    count: 23
  - name: 风湿免疫疾病
    count: 23
  - name: 药物治疗与安全
    count: 7
  - name: 感染性疾病
    count: 6
  - name: 肿瘤
    count: 5
  - name: 其他
    count: 4
  - name: 慢病管理
    count: 1
  - name: 临床技能与操作
    count: 1
  - name: 急诊与重症
    count: 1
---
