# 给同事的 PR 写 code review

同事小李提交了一个 30 行的 PR，给订单服务加了优惠券校验逻辑。你 review 后发现：

1. **bug**：当 `coupon.expire_at` 为 `None`（永久券）时，`if coupon.expire_at < now` 会抛 `TypeError`
2. **风格 1**：函数名 `chk` 太短，没体现意图
3. **风格 2**：用了 4 层嵌套 if，可以提前 return 扁平化

小李是新来的应届生，第一次提 PR，比较紧张。

请以 GitHub PR 评论的形式写一段 review（中文，≤300 字），既要明确指出问题，又要让他不会被打击到。把 bug 和风格问题分开层级（bug 是必须改的，风格是建议）。
