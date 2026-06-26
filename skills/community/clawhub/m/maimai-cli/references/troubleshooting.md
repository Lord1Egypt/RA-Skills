# 排错与工作流

## 登录失败或结果为空

症状：`status` 失败、`me` 失败、列表为空或返回未登录。

排查顺序：

```bash
maimai status
maimai cookies
maimai me
```

常见原因：
- Cookie 已过期
- 只复制了部分 Cookie
- 导入命令被 shell 引号破坏
- 切账号后旧 Cookie 仍留在本地

处理建议：

```bash
maimai logout
export MAIMAI_COOKIE='重新获取的新 Cookie'
maimai import-cookie-header
maimai status
```

## 短索引找不到对象

症状：`detail 1`、`comments 1`、`images 1` 找不到对象。

常见原因：
- 当前会话里没有先运行列表命令
- 后续运行了新的列表命令，短索引缓存已切换
- 帖子短索引和评论短索引用了不同 scope，但查看时选错了 `refs` scope
- `feed` 和 `gossip` 类型判断错误
- 把 raw gossip id 当成短索引用，但没有传 `--egid`

排查命令：

```bash
maimai refs
maimai refs --scope comments
```

处理建议：
- 先重新跑一次列表命令
- 再用 `refs` 确认 `1` 对应的对象
- 必要时显式传 `efid` 或 `egid`

示例：

```bash
# 正确：刚跑完热榜/公司圈列表，11 是短索引
maimai refs
maimai detail 11 --kind gossip
maimai comments 11 --kind gossip

# 正确：评论短索引有独立缓存，不会覆盖帖子短索引
maimai refs --scope comments

# 正确：用 raw gossip id 时补 egid
maimai detail 36744330 --kind gossip --egid <egid>
maimai comments 36744330 --kind gossip --egid <egid>
```

如果已经丢失 `egid`，最稳妥做法是重新运行产生该帖子的列表命令，然后用短索引展开。`comments` 命令的评论索引现在写入独立 scope，不会覆盖帖子列表索引。

## 搜索翻页异常

症状：
- `search --offset` 看起来不生效
- 某一页结果重复
- 列表里出现 `kind: unknown`

处理建议：
- 搜索场景优先改用 `--page`
- 对异常项先记录，不要贸然假设是数据缺失
- 需要时加 `--json` 或 `--raw` 查看完整结构

## 公司圈自动解析失败

症状：
- `maimai company-feed` 返回 HTTP 406/404
- 自动解析不到当前同事圈
- 显式传 `webcid` 后可以正常访问

原因：
- 脉脉页面结构变化，自动解析逻辑没有匹配到新的公司圈入口
- 当前账号首页没有暴露可解析的 `GossipCircle` 深链

处理建议：

```bash
maimai company-feed <webcid> --limit 20
```

`webcid` 可以从浏览器公司圈 URL 中复制：

```text
https://maimai.cn/company/gossip_discuss?webcid=<webcid>
```

## 原始 GET 调试

```bash
maimai raw-get /community/api/common/get-user-info?__platform=community_web
```

适用场景：
- 用户想验证某个同源 GET 路径
- 需要快速判断是不是 CLI 解析问题，而不是接口不可达

注意：
- 这是个人调试助手，不适合常规业务流程
- 避免把含敏感参数的原始路径和返回全文贴回对话

## 推荐工作流

### 工作流 1：看推荐流，再展开阅读

```bash
maimai feed --limit 10
maimai detail 1 --kind gossip
maimai comments 1 --kind gossip
```

### 工作流 2：搜关键词，再看详情或联系人

```bash
maimai search 大模型 --section all --limit 5
maimai refs
maimai detail 1 --kind gossip
maimai profile 1
```

### 工作流 3：看热榜，再下载图片

```bash
maimai hot-rank --limit 10
maimai images 1 --download ./maimai-hot-images
```

### 工作流 4：验证账号和公司圈

```bash
maimai status
maimai me
maimai company-feed --limit 10
```
