# 商品归类助手

这是一个基于 FastGPT 的本地 Skill。

它的流程是：

1. 用户第一次提问商品编码问题时，如果本地 SQLite 里没有该会话的手机号，就先提示输入手机号。
2. 用户发送手机号后，调用 A 智能体判断手机号是否存在。
3. 如果不存在，调用 B 智能体登记手机号。
4. 登记完成后，自动继续处理上一次待回答的商品问题。
5. 同一 `session_id` 后续再提问，直接调用 C 智能体返回商品编码答案。

## 依赖

```bash
pip install -r requirements.txt
```

## 配置

支持两种配置方式：

- 一个统一密钥：`FASTGPT_API_KEY`
- 三个独立密钥：`AGENT_A_KEY`、`AGENT_B_KEY`、`AGENT_C_KEY`

还需要：

- `FASTGPT_API_URL`
- 可选：`AGENT_A_ID`、`AGENT_B_ID`、`AGENT_C_ID`

## 本地测试

```bash
python skill.py --session-id test-user-1 --message "查一下苹果的手机壳编码"
python skill.py --session-id test-user-1 --message "13812345678"
python skill.py --session-id test-user-1 --message "华为充电器编码呢？"
```

SQLite 数据文件默认是当前目录下的 `users.db`。
