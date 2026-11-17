# 验收标准

## 功能验收

| 编号 | 验收项 | 验证方法 | 通过标准 |
|------|--------|----------|----------|
| AC1 | AK/SK 环境变量配置，不硬编码 | 检查脚本无硬编码密钥；grep AK/SK 值无匹配 | 凭据从环境变量动态扫描读取 |
| AC2 | 指标列表查询返回 JSON | `python3 scripts/huawei-cloud-ces-list.py list --region cn-north-4` | 输出 `{"count":N,"total":M,"marker":"...","metrics":[...]}` |
| AC3 | 指标数据查询返回 JSON | `python3 scripts/huawei-cloud-ces-list.py show --namespace ... --metric-name ... --dim.0 ... --filter ... --period ... --from ... --to ...` | 输出 `{"metric_name":"...","datapoints":[...]}` |
| AC4 | 指标含全部字段 | 检查 list 输出字段 | 含 namespace/dimensions/metric_name/unit 等 |
| AC5 | 支持命名空间/指标名/维度过滤 | `list --namespace SYS.ECS --metric-name cpu_util --dim.0 instance_id,xxx` | 返回过滤后结果 |
| AC6 | 无指标返回空列表 | 查询无指标的条件 | 返回 `{"count":0,"total":0,"marker":"","metrics":[]}` 非报错 |
| AC7 | 维度格式无效明确错误 | `list --dim.0 invalid_no_comma` | stderr 输出错误提示，退出码 2 |
| AC8 | AK/SK 缺失明确错误 | unset AK/SK 后执行 | stderr 输出错误提示，退出码 3 |
| AC9 | capability-list 子命令 | `python3 scripts/huawei-cloud-ces-list.py capability-list` | 输出 JSON 含 skill/service/mode/operations |
| AC10 | 独立设计 | 不依赖 scripts/greet.py | 无 import/引用现有实现 |
| AC11 | 使用说明 | `--help` / SKILL.md | 有完整使用说明 |

## 安全验收

- [ ] 无硬编码 AK/SK/Token
- [ ] 不使用 mock 模式/假数据（禁止 mock）
- [ ] 所有 API 调用有 30s 超时
- [ ] 错误处理完整（不静默崩溃）
- [ ] 参数校验防注入（维度格式校验、枚举校验）

## 结构验收

- [ ] SKILL.md ≤ 500 行，含必填段落
- [ ] frontmatter 含 name/description/version/triggers/tags
- [ ] name 与目录名一致
- [ ] references/iam-policies.md 存在
- [ ] templates/test-vars.json 存在
- [ ] 入口脚本可执行
- [ ] 总文件数 ≤ 30，总大小 ≤ 40MB
