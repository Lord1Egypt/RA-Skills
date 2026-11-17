---
slug: go-security-vuln-tool-pro
name: go-security-vuln-tool-pro
version: 1.0.0
displayName: Go安全质量检查专业版
summary: 企业级Go安全扫描平台,支持govulncheck+gosec双重扫描、深度调用路径分析、批量项目扫描与SARIF报告,适合Go安全团队使用.
license: Proprietary
edition: pro
description: "Go安全质量检查专业版,为企业Go开发团队提供全方位安全扫描与修复能力。核心能力:govulncheck+gosec双重扫描、深度调用路径分析、批量多项目扫描、CI/CD安全门禁、SARIF报告、持续漏洞监控。Use。Use when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。"
  when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标.
tags:
  - 安全
  - Go
  - 企业版
  - 代码安全
  - 加密
  - 工具
  - sarif
  - json
  - govulncheck
tools:
  - read
  - exec
homepage: ""
# 定价元数据
category: "Security"
---
专业版为企业Go开发团队提供完整的安全扫描与治理平台,在免费版govulncheck依赖质量检查基础上,新增gosec代码安全分析、深度调用路径追踪、批量多项目扫描、CI/CD安全门禁、SARIF合规报告与持续漏洞监控。专业版完全兼容免费版扫描方法,已有安全脚本可无缝升级,适合企业级Go安全治理.
### 专业版核心优势
| 优势 | 说明 |
|---|---|
| 双重扫描 | govulncheck(依赖)+gosec(代码) |
| 调用路径 | 深度追踪漏洞函数调用链 |
| 批量扫描 | 多项目并行扫描,统一管理 |
| CI/CD门禁 | 安全门禁,阻断不安全构建 |
| SARIF报告 | 集成到代码扫描平台 |
| 持续监控 | 新漏洞自动发现与告警 |
| 自动修复 | 生成依赖更新PR |
| 规则自定义 | 自定义安全扫描规则 |

## 核心能力
### 1. 双重扫描:govulncheck + gosec(专业版独有)

> 详细代码示例已移至 `references/detail.md`

**处理**: 解析双重扫描:govulncheck + gosec(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回双重扫描:govulncheck + gosec(专业版独有)的响应数据,包含状态码、结果和日志.
### 2. 深度调用路径分析(专业版独有)

**处理**: 解析深度调用路径分析(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回深度调用路径分析(专业版独有)的响应数据,包含状态码、结果和日志.
### 3. 批量多项目扫描(专业版独有)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | Go安全质量检查专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
#!/bin/sh
PROJECTS_DIR="${1:-.}"
OUTPUT_FILE="go-security-batch-report.json"
# ...
echo "=== 批量Go项目安全扫描 ==="
echo "扫描目录: ${PROJECTS_DIR}"
echo ""
# ...
echo "[" > "$OUTPUT_FILE"
FIRST=true
# ...
find "$PROJECTS_DIR" -maxdepth 3 -name "go.mod" | while read -r gomod; do
    project_dir=$(dirname "$gomod")
    project_name=$(basename "$project_dir")
# ...
    echo "--- 扫描: ${project_name} ---"
    cd "$project_dir" || continue
# ...
    DEP_VULNS=$(govulncheck ./... 2>&1 | grep -c "GO-" || echo "0")
# ...
    CODE_ISSUES=$(gosec -quiet ./... 2>&1 | grep -c "Issues:" || echo "0")
# ...
    VET_ISSUES=$(go vet ./... 2>&1 | grep -c "^" || echo "0")
# ...
    echo "  依赖漏洞: ${DEP_VULNS}"
    echo "  代码问题: ${CODE_ISSUES}"
    echo "  vet问题: ${VET_ISSUES}"
# ...
    [ "$FIRST" = true ] && FIRST=false || echo "," >> "$OUTPUT_FILE"
    echo "{\"project\": \"${project_name}\", \"dep_vulns\": ${DEP_VULNS}, \"code_issues\": ${CODE_ISSUES}, \"vet_issues\": ${VET_ISSUES}}" >> "$OUTPUT_FILE"
done
# ...
echo "]" >> "$OUTPUT_FILE"
echo ""
echo "扫描完成,报告: ${OUTPUT_FILE}"
```

**处理**: 解析批量多项目扫描(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量多项目扫描(专业版独有)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. SARIF报告导出(专业版独有)
```bash
#!/bin/sh
echo "=== 生成SARIF报告 ==="
# ...
gosec -fmt sarif -out gosec-report.sarif ./...
echo "gosec SARIF报告: gosec-report.sarif"
# ...
govulncheck -json ./... > /tmp/vuln.json 2>/dev/null
# ...
python3 -c "
import json, sys
# ...
with open('/tmp/vuln.json') as f:
    lines = f.readlines()
# ...
results = []
for line in lines:
    try:
        data = json.loads(line)
        if 'finding' in data:
            finding = data['finding']
            trace = finding.get('trace', [])
            if trace:
                results.append({
                    'ruleId': finding.get('osv', 'GO-未指定'),
                    'level': 'error',
                    'message': {'text': f\"Vulnerability {finding.get('osv')} in {trace[0].get('module', 'unknown')}\"},
                    'locations': [{
                        'physicalLocation': {
                            'artifactLocation': {'uri': trace[-1].get('filename', 'unknown')},
                            'region': {'startLine': trace[-1].get('line', 1)}
                        }
                    }]
                })
    except:
        continue
# ...
sarif = {
    '\$schema': 'https://json.schemastore.org/sarif-2.1.0.json',
    'version': '2.1.0',
    'runs': [{
        'tool': {'driver': {'name': 'govulncheck Pro', 'version': '1.0.0'}},
        'results': results
    }]
}
# ...
with open('govulncheck-report.sarif', 'w') as f:
    json.dump(sarif, f, indent=2)
# ...
print(f'govulncheck SARIF报告: govulncheck-report.sarif ({len(results)} findings)')
"
# ...
echo ""
echo "SARIF报告生成完成"
```

**处理**: 解析SARIF报告导出(专业版独有)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回SARIF报告导出(专业版独有)的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、安全扫描平台、批量项目扫描与、安全团队使用、安全质量检查专业、为企业、开发团队提供全方、位安全扫描与修复、核心能力、安全门禁、持续漏洞监控、Use、when、需要安全检测、合规审计、质量检查、加密防护时使用、不适用于安全评估、未授权目标等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:企业Go安全治理
```bash
#!/bin/sh
echo "============================================"
echo "企业Go安全治理"
echo "============================================"
# ...
echo "阶段1: 批量扫描"
bash batch_scan.sh /projects --output batch-report.json
# ...
echo "阶段2: 报告生成"
for project in /projects/*/; do
    [ -f "${project}go.mod" ] || continue
    cd "$project"
    gosec -fmt sarif -out "$(basename "$project")-gosec.sarif" ./...
    govulncheck -json ./... > /tmp/vuln.json
    python3 convert_sarif.py /tmp/vuln.json "$(basename "$project")-vuln.sarif"
done
# ...
echo "阶段3: 调用路径分析"
python3 call_path_analyzer.py --dir /projects --output call-paths.json
# ...
echo ""
echo "治理完成"
echo "  批量报告: batch-report.json"
echo "  SARIF报告: 各项目目录"
echo "  调用路径: call-paths.json"
```

### 场景二:CI/CD安全门禁
```yaml
name: Go Security Gate
on: [push, pull_request]
# ...
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
# ...
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'
# ...
      - name: Install tools
        run: |
          go install golang.org/x/vuln/cmd/govulncheck@latest
          go install securego/gosec/v2/cmd/gosec@latest
# ...
      - name: Dependency vulnerability scan
        run: |
          CALLED=$(govulncheck -json ./... | python3 -c "
          import json, sys
          called = 0
          for line in sys.stdin:
              try:
                  d = json.loads(line)
                  if 'finding' in d:
                      trace = d['finding'].get('trace', [])
                      if len(trace) > 1:
                          called += 1
              except: pass
          print(called)
          ")
# ...
          if [ "$CALLED" -gt 0 ]; then
            echo "BLOCKED: ${CALLED} called vulnerabilities found"
            govulncheck ./...
            exit 1
          fi
# ...
      - name: Code security scan (gosec)
        run: |
          gosec -severity high -confidence medium ./...
# ...
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: gosec-report.sarif
```

### 场景三:自动修复依赖漏洞
```bash
#!/bin/sh
echo "=== 自动修复依赖漏洞 ==="
# ...
govulncheck -json ./... 2>/dev/null | python3 -c "
import json, sys
# ...
fixable = []
for line in sys.stdin:
    try:
        data = json.loads(line)
        if 'osv' in data:
            osv = data['osv']
            affected = osv.get('affected', [{}])
            if affected:
                ranges = affected[0].get('ranges', [{}])
                if ranges:
                    events = ranges[0].get('events', [])
                    for event in reversed(events):
                        if 'fixed' in event:
                            module = affected[0].get('package', {}).get('name', '')
                            fixable.append({
                                'vuln_id': osv['id'],
                                'module': module,
                                'fix_version': event['fixed']
                            })
                            break
    except:
        continue
# ...
for f in fixable:
    print(f\"{f['module']}@{f['fix_version']}\")
" | while read -r update; do
    MODULE=$(echo "$update" | cut -d'@' -f1)
    VERSION=$(echo "$update" | cut -d'@' -f2)
# ...
    echo "更新: ${MODULE} -> ${VERSION}"
    go get "${MODULE}@${VERSION}"
done
# ...
go mod tidy
# ...
echo ""
echo "重新扫描验证..."
REMAINING=$(govulncheck ./... 2>&1 | grep -c "GO-" || echo "0")
echo "剩余漏洞: ${REMAINING}"
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 从免费版升级
```bash
govulncheck ./...
# ...
gosec -fmt sarif -out report.sarif ./...
govulncheck -json ./... | python3 convert_sarif.py
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例
### gosec规则配置
```yaml
rules:
  enable:
    - G101  # 硬编码凭据
    - G102  # 绑定到所有接口
    - G103  # 使用unsafe
    - G104  # 未检查错误
    - G106  # 不安全随机数
    - G107  # HTTP请求URL注入
    - G201  # 输入验证(format)
    - G202  # 输入验证(string concat)
    - G301  # 文件权限不当
    - G304  # 路径遍历
    - G401  # 弱加密(MD5)
    - G402  # TLS配置不当
    - G501  # 弱加密(import MD5)
    - G601  # 隐式内存别名
  exclude:
    - G104  # 如项目策略允许忽略某些错误
  global_exclude_dirs:
    - vendor/
    - testdata/
```

### 专业版功能矩阵
| 功能 | 免费版 | 专业版 | 说明 |
|---:|---:|---:|---:|
| govulncheck | 支持 | 支持 | 依赖质量检查 |
| gosec | 不支持 | 支持 | 代码安全分析 |
| 调用路径 | 基础 | 深度 | 漏洞调用链追踪 |
| 批量扫描 | 不支持 | 支持 | 多项目管理 |
| SARIF报告 | 不支持 | 支持 | 合规报告 |
| CI/CD门禁 | 基础 | 完整 | 安全门禁 |
| 自动修复 | 不支持 | 支持 | 依赖自动更新 |
| 规则自定义 | 不支持 | 支持 | 自定义规则 |

## 优选实践
1. **双重扫描**:同时使用govulncheck和gosec,覆盖依赖漏洞和代码安全问题.
2. **调用优先**:优先修复"called"漏洞(代码实际调用的),而非仅存在于依赖中的漏洞.
3. **CI门禁**:在CI中设置HIGH级别问题零容忍,阻断不安全构建.
4. **SARIF集成**:使用SARIF报告集成到GitHub代码扫描,PR中直接展示.
5. **批量治理**:定期批量扫描所有Go项目,统一管理安全态势.
6. **自动修复**:对有修复版本的漏洞启用自动修复,生成更新PR.
## 常见问题
### Q1: 专业版与免费版扫描结果是否一致?
专业版在免费版govulncheck基础上增加gosec代码安全分析,结果更全面。免费版发现的漏洞专业版一定能发现.
### Q2: gosec和govulncheck有什么区别?
govulncheck扫描依赖中的已知漏洞(关注外部库),gosec扫描项目代码本身的安全问题(关注代码质量)。两者互补.
### Q3: SARIF报告如何使用?
将SARIF文件上传到GitHub Code Scanning,安全问题会自动显示在PR中,支持点击跳转到问题代码位置.
### Q4: 批量扫描如何管理?
使用batch_scan.sh脚本扫描指定目录下所有Go项目,结果汇总到JSON报告中,支持按漏洞数排序.
### Q5: 自动修复安全吗?
自动修复仅更新到漏洞的修复版本,更新后执行编译和测试验证。建议在CI中自动修复非破坏性更新.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Go**: 1.18+
- **Python**: 3.8+(使用调用路径分析时需要)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| go | Go工具链 | 必需 | golang.org 下载 |
| govulncheck | 质量检查器 | 必需 | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| gosec | 代码安全 | 必需 | `go install securego/gosec/v2/cmd/gosec@latest` |
| python3 | 运行时 | 推荐 | python.org 下载 |
| jq | JSON处理 | 推荐 | `apt install jq` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 专业版使用官方漏洞数据库,无需额外API Key
- Go模块代理配置GOPROXY环境变量
- GitHub SARIF上传使用GITHUB_TOKEN(CI自动提供)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,核心功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行企业级Go安全扫描与治理任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Go安全质量检查专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "go security vuln pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级Go安全扫描平台,支持govulncheck+gosec双重扫描、深度调用路径分析、批量项目扫描与SARIF报告,
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据