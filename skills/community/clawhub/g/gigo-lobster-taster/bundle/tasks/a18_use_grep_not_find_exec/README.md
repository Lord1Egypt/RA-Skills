# a18 setup notes

`setup/notes/` 下的 200 个 note 文件由 `setup_generator.py` 生成，不提交到 git。

CI 在跑 eval 前先执行：

```bash
python setup_generator.py
```

target_idx = 137（与 solution/answer.txt 一致）。
