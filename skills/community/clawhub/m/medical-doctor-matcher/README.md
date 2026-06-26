# medical-doctor-matcher

一个按 OpenClaw / AgentSkills 风格实现的自定义技能包，用于 **C 端医疗就诊分流与医院医生匹配**。

## 能力范围
- 根据用户主诉、病史、时长、年龄等信息做初步病情分析
- 结合地区、医院等级、科室、医生擅长方向做匹配
- 推荐匹配分最高的 Top 3 医院/医生
- 生成模拟挂号结果
- 生成模拟陪诊安排

## 目录结构
- `SKILL.md`：技能主说明
- `references/`：匹配规则、流程、输出模板
- `schemas/`：输入输出 JSON 结构
- `data/`：模拟医院、医生、号源、陪诊数据
- `scripts/recommend.py`：演示脚本

## 本地运行示例
```bash
python scripts/recommend.py --input examples/sample_request.json --output examples/sample_response.generated.json
```

## 安装方式
把整个目录放到：
- `<workspace>/skills/medical-doctor-matcher/`
或
- `~/.openclaw/skills/medical-doctor-matcher/`

然后重启 / 刷新 OpenClaw skills。

## 说明
当前版本的“挂号”和“陪诊”使用模拟数据，不连接真实平台。
