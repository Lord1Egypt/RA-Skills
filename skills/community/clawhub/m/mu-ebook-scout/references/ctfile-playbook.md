# ctfile 城通网盘直链获取 Playbook

> 用于 skill 工作流第 4 步：用户明确要求 agent 代取网盘文件时。
> 需要浏览器环境（任意浏览器自动化工具，如 Playwright 或浏览器 MCP）。

## 背景

`github_lists` 源返回的城通链接形如
`https://url89.ctfile.com/f/{userid}-{fileid}-{hash}?p=8866`
（`p=` 后是提取码，常见 `8866`）。页面跳转到 z701.com。

## 流程

### Step 1：导航并确认文件

打开链接并确认文件（以 Playwright 为例）：

```python
page.goto("<ctfile链接>")
```

也可在普通浏览器中打开。确认文件名与大小（若密码框出现，
填入提取码后点「解密文件」；`?p=` 参数通常自动带入，无需重复输入）。

### Step 2：页面变量提取（浏览器 console / evaluate）

```javascript
JSON.stringify({
  api_server: typeof api_server !== 'undefined' ? api_server : '',
  userid: typeof userid !== 'undefined' ? userid : '',
  file_id: typeof file_id !== 'undefined' ? file_id : '',
  share_id: typeof share_id !== 'undefined' ? share_id : '',
  file_chk: typeof file_chk !== 'undefined' ? file_chk : '',
  start_time: typeof start_time !== 'undefined' ? start_time : '',
  wait_seconds: typeof wait_seconds !== 'undefined' ? wait_seconds : '',
  verifycode: typeof verifycode !== 'undefined' ? verifycode : ''
})
```

### Step 3：API 取直链（浏览器 console / evaluate，async IIFE）

```javascript
(async () => {
  try {
    var url = api_server + '/get_file_url.php?uid=' + userid
      + '&fid=' + file_id + '&folder_id=0&share_id=' + share_id
      + '&file_chk=' + file_chk + '&start_time=' + start_time
      + '&wait_seconds=' + wait_seconds + '&mb=0&app=0&acheck=0'
      + '&verifycode=' + verifycode + '&rd=' + Math.random();
    var headers = typeof getAjaxHeaders === 'function' ? getAjaxHeaders() : {};
    var resp = await fetch(url, {headers: headers});
    return JSON.stringify(await resp.json());
  } catch(e) { return 'Error: ' + e.message; }
})()
```

`code: 200` → `downurl` 即直链（有时效性，拿到后立即下载）。

### Step 4：curl 下载 + 校验

```bash
curl -L -o "书名.zip" "<downurl>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://z701.com/" --max-time 300
file "书名.zip"   # 必须是 Zip archive；若显示 HTML 说明直链过期，回 Step 3
```

### Step 5：GBK 解压 + 魔数校验

```python
import zipfile, os
z = zipfile.ZipFile("书名.zip")
for info in z.infolist():
    if info.filename.endswith((".epub", ".mobi", ".azw3", ".pdf")):
        with z.open(info) as src:
            open(os.path.basename(info.filename), "wb").write(src.read())
```

对解压文件跑 `bookscout` 的 `sniff_format`（EPUB=PK、MOBI=BOOKMOBI@60、
PDF=%PDF）后交付。文件保存在用户工作区内。

## 常见坑

| 现象 | 处理 |
|---|---|
| API 返回 code != 200 | 看 wait_seconds，等待后重试一次 |
| downurl 403 | 补 Referer: https://z701.com/ 头 |
| zip 解出来是 HTML | 直链过期，从 Step 3 重新取 |
| 链接 404 | 网盘资源已删，回搜索换其他 hit |
