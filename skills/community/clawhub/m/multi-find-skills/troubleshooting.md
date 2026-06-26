# 故障排除指南

## 找不到结果

**首先：** 尝试替代搜索词（同义词、英文翻译、更具体的描述）。

**如果仍然没有：**

1. **诚实承认**
   > "我在配置来源中搜索了与 [X] 相关的技能，但没有找到强匹配。"

2. **提供直接帮助**
   > "我可以用自己的能力直接帮你处理这个。"

3. **建议创建（对于重复需求）**
   > "如果你经常做这个，可以用 `skill-creator` 创建一个自定义技能。"

## 结果太多

**问题：** 搜索返回 10+ 个技能，难以选择。

**解决方案：**
1. 应用质量过滤器（见 `evaluation.md`）
2. 检查 `memory.md` 中的偏好
3. 仅呈现前 3 名并清晰区分
4. 如果仍然不清楚，提出澄清问题

> "找到几个选项。为了缩小范围：
> - 需要基本功能还是全面的？
> - 偏好流行/稳定还是前沿？"

## 找不到技能（404）

**可能原因：**
- slug 拼写错误
- 技能已被删除/隐藏
- 作者更改了名称
- Skills.sh 结果指向已更改的仓库或技能路径

**解决方案：**
1. 改用描述搜索而非确切的名称
2. 检查类似名称：`clawhub search "partial-name"`
3. 如果缺失结果来自 Skills.sh，重新运行 `npx skills find [domain]`
4. 技能可能已被替换 — 搜索该领域

## 过时的技能

**迹象：**
- 最后更新 >6 个月前
- 最近下载量低
- 引用工具的旧版本

**处理方式：**
> "这个技能最后更新于 [X 个月前]。它引用了 [旧版本]。仍然要试试，还是我找替代？"

## 来源不匹配

**问题：** 结果在一个生态系统中找到，但显示的安装命令属于另一个。

**解决：**
1. 重新明确说明来源
2. 仅使用属于该来源的安装命令
3. 如需要，从另一个生态系统呈现等效结果

> "这个结果来自 Skills.sh，所以正确的安装路径是 `npx skills add owner/repo@skill`，而不是 `clawhub install`。"

## 技能被标记为可疑

**含义：** VirusTotal Code Insight 检测到潜在风险模式（API 调用、文件访问等）。

**处理方式：**

1. **告知用户**
   > "这个技能被安全扫描器标记为可疑。它可能进行外部 API 调用或访问文件。"

2. **检查触发原因**
   ```bash
   npx clawhub inspect <slug> --files
   ```

3. **默认选择更安全的替代方案**
   > "我可以推荐未标记的类似技能，然后我们选最佳匹配。"

4. **禁止行为**
   - ❌ 永远不要使用强制安装选项（`--force`）
   - ❌ 跳过扫描器警告
   - ❌ 在用户未明确同意前安装可疑技能

## 冲突的技能

**问题：** 用户想要的技能与已安装的技能功能重叠。

**检测：** 检查 `npx clawhub list` 中同领域的现有技能。

**解决：**
1. **解释重叠**
   > "你已安装了 `git`。`github` 技能在此基础上添加 PR/issue 功能——它们配合使用。"

2. **或警告冲突**
   > "你已安装了 `eslint-basic`。`eslint-pro` 覆盖相同内容但更全面——要替换吗？"

## 用户改变主意

**安装后想卸载：**
```bash
clawhub uninstall <slug>           # ClawHub 安装
npx skills remove <skill>         # Skills.sh 安装
```

**不想装了：** 添加到 `memory.md` 的 `Passed` 并附原因，避免下次再推荐。

## 记忆文件问题

**记忆文件损坏或格式错误：**
1. 备份：`cp ~/.openclaw/skills/multi-find-skills/memory.md ~/.openclaw/skills/multi-find-skills/memory.md.bak`
2. 根据 `memory-template.md` 重新创建
3. 请用户重新说明关键偏好

**记忆太大（>50 行）：**
1. 归档旧条目
2. 仅保留最近的 Liked/Passed
3. 保留所有 Preferences（它们是稳定的）

---

## 搜索质量问题

### ClawHub 搜索无结果

**原因**：网络连接问题、关键词不够具体、速率限制触发

**解决方案**：
```bash
# 1. 检查网络
curl -I https://clawhub.ai

# 2. 尝试不同关键词（同义词/英文）
clawhub search "weather"          # 尝试英文
clawhub search "tavily search"    # 尝试具体名称

# 3. 浏览热门技能发现新选项
clawhub explore --sort installs --limit 20

# 4. 手动访问网站搜索
open https://clawhub.ai
```

### skills.sh 搜索无结果

**原因**：`npx` 不可用、网络问题、包名/关键词不正确

**解决方案**：
```bash
# 1. 确认 npx 可用
npx --version

# 2. 尝试更通用的关键词
npx skills find "web"

# 3. 使用完整包名
npx skills find "vercel-labs/agent-skills@seo-best-practices"
```

### LobeHub 搜索无结果

**原因**：`npx` 不可用、网络问题

**解决方案**：
```bash
# 1. 确认 npx 可用
npx --version

# 2. 尝试网页搜索
open https://lobehub.com/skills?q=<关键词>
```

### 搜索结果质量低

**原因**：关键词太泛、相关技能确实不存在

**解决方案**：
```bash
# 1. 使用更具体的关键词
clawhub search "seo audit"       # 比 "seo" 更具体
clawhub search "web scraping"     # 比 "web" 更具体

# 2. 尝试多个相关关键词
clawhub search "weather"
clawhub search "weather forecast"
clawhub search "weather api"

# 3. 浏览热门技能发现灵感
clawhub explore --sort installs --limit 20
```

## 安装问题

### 安装失败

**原因**：网络问题、权限问题、包名错误、安装到错误路径

**解决方案**：
```bash
# 1. 检查 ~/.openclaw/skills/ 是否可写
ls -la ~/.openclaw/skills/

# 2. 使用 --force 重试
clawhub install <skill-name> --force

# 3. 确认包名正确
clawhub search "<关键词>"  # 确认精确包名

# 4. 使用中国镜像（网络问题）
clawhub install <skill-name> --registry https://cn.clawhub-mirror.com
```

### 安装后验证失败

**原因**：安装实际失败但无报错、安装到了错误路径

**解决方案**：
```bash
# 1. 检查是否安装到了正确路径
ls ~/.openclaw/skills/<skill-name>/SKILL.md  # 正确路径
ls ~/.openclaw/<skill-name>/SKILL.md         # 错误路径

# 2. 如果安装到错误路径，手动移动
mv ~/.openclaw/<skill-name> ~/.openclaw/skills/<skill-name>/

# 3. 重新安装
clawhub install <skill-name> --force
```

### 速率限制

**解决方案**：
```bash
# 1. 等待 1 小时后再试
sleep 3600

# 2. 使用替代来源（网站搜索）
open https://clawhub.ai/search?q=<关键词>

# 3. 使用 GitHub 手动搜索
open https://github.com/search?q=openclaw+skill+<关键词>
```

## 命令参数错误

**症状**：执行命令时报 `unknown option '--sort'` 等错误

**原因**：使用了不存在的命令参数

**解决方案**：
```bash
# 排序应使用 explore 命令，不是 search
clawhub explore --sort installs --limit 20  # ✅ 正确

# 不是
clawhub search --sort installs              # ❌ 错误
```