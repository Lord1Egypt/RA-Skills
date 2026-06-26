# 安全审查清单

审查对象：`scripts/` 下全部 `.py` 脚本 + `common.py`。

---

## 一、命令注入

- [ ] **subprocess shell=True**：列出所有使用处，确认用户输入经过验证/过滤
- [ ] **os.system / os.popen**：确认无残留调用
- [ ] **f-string / .format 拼接命令**：确认拼接的变量已做安全处理
- [ ] **过滤完整性**：shell=True 的过滤是否覆盖 `` ` ``、`$(`、`${`、`;`、`&&`、`||`
- [ ] **private _run_cmd**：确认与 common.py 过滤逻辑一致，或直接改用 common.run_cmd

## 二、路径遍历

- [ ] **文件写入路径**：所有接收用户路径参数的写入操作，是否限制在安全目录（Home/Temp/CWD）
- [ ] **路径规范化**：是否使用 os.path.realpath 解析后校验
- [ ] **`..` 检测**：路径是否拒绝包含 `..` 的组件

## 三、PowerShell 注入

- [ ] **用户输入嵌入 PS 脚本**：是否做了转义（单引号用 `''` 转义，双引号用 `` `" `` 转义）
- [ ] **正则操作数**：用户输入用于 `-match`/`-replace` 时是否转义正则特殊字符
- [ ] **危险模式拦截**：common.py 的 `run_ps` 是否拦截了 `--%`、`cmd /c`、`iex`、`Start-Process -FilePath`

## 四、输入验证

- [ ] **argparse 参数**：所有接收用户输入的参数是否在传入命令前验证（类型、格式、长度）
- [ ] **特殊格式**：MAC 地址、UUID、GPU ID 等是否有正则校验
- [ ] **白名单**：枚举类参数（如 query_fields）是否使用白名单而非直接传递

## 五、依赖安全

- [ ] **pip install 版本锁定**：所有 `pip install` 调用是否指定了最低+最高版本（如 `>=x,<y`）
- [ ] **无 eval/exec**：搜索 `eval(`、`exec(`、`__import__`，确认无动态代码执行
