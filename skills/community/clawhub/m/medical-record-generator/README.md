# 病历生成器技能

这是一个专业的病历撰写助手，按照三步流程生成规范的入院记录。

## 功能特点

1. **三步流程**：收集变量 → 询问补充 → 生成记录
2. **专业模板**：符合医疗规范的入院记录格式
3. **可执行脚本**：包含完整的病历生成JavaScript代码
4. **易于集成**：可作为OpenClaw技能使用

## 使用方法

### 作为OpenClaw技能
当用户触发以下关键词时自动激活：
- "写病历"
- "生成病历" 
- "病历助手"
- "入院记录"
- "medical record"
- "病历生成"

### 作为独立脚本
```javascript
const MedicalRecordGenerator = require('./scripts/generate_record.js');
const generator = new MedicalRecordGenerator();

const data = {
  name: "患者姓名",
  gender: "性别",
  age: "年龄",
  chiefComplaint: "主诉",
  preliminaryDiagnosis: "初步诊断"
};

const record = generator.generateRecord(data);
console.log(record);
```

## 文件结构

```
medical-record-generator/
├── SKILL.md              # 技能说明文件
├── package.json          # 包配置文件
├── scripts/
│   └── generate_record.js # 病历生成核心脚本
├── references/
│   └── example.md        # 使用示例
└── assets/               # 资源文件目录
```

## 许可证
MIT