# 账号与授权

客户端将轻页凭证存入 ~/.config/litepage，目录 0700、文件 0600；LITEPAGE_CONFIG_DIR 可隔离测试配置。与 Echo CLI 凭证目录分开，按 API 实例分隔，托管凭证只能操作轻页。

当前 Skill 使用无固定到期时间的设备凭证，关闭 Agent 或间隔 30 天以上可复用。官方默认入口升级为轻页域名时，若尚无新入口凭证或待完成登录，会自动沿用 ~/.config/litepage 中旧 echo.hqdx.store 的设备文件与锁，无需扫码、不复制 token；已有新入口凭证优先。此兼容仅限两个已知官方 API，不读取 Echo CLI 的凭证，自定义实例仍隔离。显式退出、撤销或删除凭证后需重新登录。

第一次发布自动创建匿名身份。匿名凭证是恢复依据；凭证全部丢失且未绑定微信，作品无法恢复管理。明确失效的凭证不能通过静默新建匿名身份绕过。

```bash
python3 "/实际skill目录/scripts/litepage.py" claim 作品UUID
python3 "/实际skill目录/scripts/litepage.py" bind-wechat
python3 "/实际skill目录/scripts/litepage.py" login --wechat
python3 "/实际skill目录/scripts/litepage.py" logout
```

发布成功返回 creator.claim_url，客户端还生成私有本地二维码 creator.qr_path。Agent 应直接展示二维码图片，并附认领页链接、有效期及核对码；核对码只用于比对，不要求输入。PC 打开链接会看到轻页扫码页，微信内打开或扫码才跳转公众号授权；普通手机浏览器显示在微信中打开或截图识别的指引。扫码页的读取/刷新不创建或轮换 OAuth state，不影响手机正在进行的授权；确认和有效期仍由服务端校验。用户在轻页授权页（lightpage.hqdx.store）用微信核对并确认后，服务端完成归属变更；Agent 可以已结束运行，不需要等待或领取新 token。认领链接短期有效且仅给创作者本人，单凭公开作品链接不能认领。claim 命令验证当前凭证是作品所有者后复用仍处于 pending 的有效入口，或生成新入口，已绑定返回 claimed。它不上传或改变作品版本。

bind-wechat 是另一个主动等待扫码的入口，将当前匿名身份资产归入用户确认的微信身份，保留作品链接，已有设备仍保留各自产品权限；login --wechat 用于另一设备恢复。微信已有身份时按 Echo 的规则合并匿名资产与设备，不是只复制当前项目。首次微信会自动创建账号，已有微信账号则直接归并；确认页明确全部作品的归并范围。普通发布仅附认领入口，不强制扫码；用户主动要求绑定或恢复时才执行等待型登录命令。

bind-wechat 和 login --wechat 的 stderr 输出 authorization_required 事件，包含 qr_path、user_code、expires_in。直接展示该本地二维码图片，让用户亲自在微信核对并确认。保留等待中的进程，不替用户批准、不重复发起。拒绝或过期后报告，用户要求继续时重启登录。token 不得展示或复制进作品。

logout 撤销当前设备并删除本地凭证，不删除作品。官网和管理台均使用轻页域名，管理台通过微信登录管理同一身份；匿名作品先通过发布时的私有认领入口完成微信绑定，才能在微信登录后看到。原设备 token 不变，本地缓存的 identity_type 可能仍为 anonymous；以服务端 claim / me 的结果为准，不因此重复注册。

认领 URL 的 10 位短码与 verification_code 不是同一个值。二维码编码完整 claim_url；核对码只用于在手机确认页比对，无需输入或自行从 URL 末尾计算。旧 UUID 认领链接仍可打开，所有入口保持原有效期。

网页操作：打开 [轻页首页](https://lightpage.hqdx.store/)，点击顶部“我的作品”进入 [个人管理页](https://lightpage.hqdx.store/manage/)，再点击“微信登录”并由用户扫码确认。网页登录与 CLI 登录各自保存设备凭证；不复制 token，使用同一微信即可管理认领后的作品。查询与数据说明见[作品管理与统计](management.md)。
