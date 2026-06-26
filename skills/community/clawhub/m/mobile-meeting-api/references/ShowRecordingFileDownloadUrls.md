# 查询录制文件下载链接 - ShowRecordingFileDownloadUrls<a name="ZH-CN_TOPIC_0000001107892998"></a>

## 描述<a name="section17948858131615"></a>

该接口用于查询指定会议录制文件下载链接。

>![](public_sys-resources/icon-note.gif) **说明：** 
>-   仅企业管理员权限的账号才能查询录制文件的下载链接


## URI<a name="section11103208192715"></a>

GET /v1/mmc/management/record/downloadurls

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| confUUID | 是 | String | Query | 会议UUID(通过 查询录制列表 获取)。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。 |
| limit | 否 | Integer | Query | 查询数量。默认是20，最大500条。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section963985011428"></a>

**表 2**  状态码说明

<a name="table102780442391"></a>

| HTTP状态码 | 描述 |
|---|---|
| 200 | 操作成功。 |
| 400 | 参数异常。 |
| 401 | 未鉴权或鉴权失败。 |
| 403 | 权限受限。 |
| 500 | 服务端异常。 |


## 响应参数<a name="section498722842014"></a>

**表 3**  响应参数

<a name="table6981112405218"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| recordUrls | Array of DownloadInfo objects | 会议录制文件下载链接信息。 |


**表 4**  DownloadInfo数据结构

<a name="table965442515915"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| confUuid | String | 会议UUID。 |
| urls | Array of UrlInfo objects | 下载链接信息。 |


**表 5**  UrlInfo数据结构

<a name="table5334113071114"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| token | String | 下载鉴权token，下载文件时，使用该token鉴权。（一小时内有效，使用后立即失效）。 |
| fileType | String | 文件类型。 Aux：辅流（会议中的共享画面；分辨率为720p） Hd：高清（会议中的视频画面；分辨率和会议中视频画面的分辨率一致，1080p或者720p） Sd：标清（会议中视频画面和共享画面的合成画面，视频画面是大画面，共享画面是小画面，共享画面布局在右下方；分辨率为4CIF） 说明： 单会议录制时长超过3小时将拆分成多个文件，有多个下载链接（旧版录制文件仍按1GB拆分）。 |
| url | String | 文件下载url，最大1000个字符。 |


## 请求消息示例<a name="section1498763918202"></a>

```
GET /v1/mmc/management/record/downloadurls?confUUID=51adf610220411eaaae03f22d33cc26b
Connection: keep-alive
X-Access-Token: stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 505
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: 4556e88832e5990723d1712395f5bee8
Server: api-gateway
X-Request-Id: 629891c82bb852d8796e2f6acc74721e

{
    "recordUrls": [
        {
            "confUuid": "ef67f6ada67e11eba6374db4b9a61d2c",
            "urls": [
                {
                    "token": "f8fe906eaa6d690ef72bc831df54ffd9fc906412aefd329ace96d100cf1bc4be",
                    "fileType": "Aux",
                    "url": "https://100.85.230.37/download/typeThree/video/resource/00037/00037ed2-351a-4741-8ce6-a2078f21ba6b/videoAux/0_0.mp4"
                },
                {
                    "token": "ad8a6f6e009d643ca21f8be306e9e2cadd726360236f07bd176c1b85423b7136",
                    "fileType": "Hd",
                    "url": "https://100.85.230.37/download/typeThree/video/resource/00037/00037ed2-351a-4741-8ce6-a2078f21ba6b/videoHD/0_0.mp4"
                },
                {
                    "token": "fe7a59c69e3f97e831c83d55193a061e5e33e019f4704e5eb441c7f1fa629ad2",
                    "fileType": "Sd",
                    "url": "https://100.85.230.37/download/typeThree/video/resource/00037/00037ed2-351a-4741-8ce6-a2078f21ba6b/videoSD/0_0.mp4"
                },
                {
                    "token": "38e6b3fe7f7c62dd2141a408f4f64b911d1b58a5e04a4f6e0cfd2602181a8ad3",
                    "fileType": "Aux",
                    "url": "https://100.85.230.37/download/typeThree/video/resource/00037/00037ed2-351a-4741-8ce6-a2078f21ba6b/videoAux/0_1.mp4"
                },
                {
                    "token": "843731642aba1ebb720195a7c44f3f1e32ab409d29b2ecd1c58f30ee269f6da6",
                    "fileType": "Hd",
                    "url": "https://100.85.230.37/download/typeThree/video/resource/00037/00037ed2-351a-4741-8ce6-a2078f21ba6b/videoHD/0_1.mp4"
                },
                {
                    "token": "9fd3471e9dc047c3c345308f0cbed005f227bf48aa47875c7fe752c5a817cbd9",
                    "fileType": "Sd",
                    "url": "https://100.85.230.37/download/typeThree/video/resource/00037/00037ed2-351a-4741-8ce6-a2078f21ba6b/videoSD/0_1.mp4"
                }
            ]
        }
    ]
}
```

## 下载示例<a name="section450918479153"></a>

通过调用接口，获取到下载链接和鉴权token后，可以通过以下示例代码（Java）下载录制文件：

```
/**
 * 录制文件下载
 *
 * @param downloadUrl 录制文件下载链接
 * @param localPath   本地保存路径
 * @param token 下载鉴权token
 */
public static void httpDownload(String downloadUrl, String localPath, String token) {
    int byteRead;
    try {
        URL url = new URL(downloadUrl);
        HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
        // 请求头域中携带下载鉴权token
        connection.setRequestProperty("Authorization", token);
        connection.setHostnameVerifier(new HostnameVerifier() {
            @Override
            public Boolean verify(String hostname, SSLSession sslSession) {
                return true;
            }
        });
        TrustManager[] trustManagers = new TrustManager[]{
                new X509TrustManager() {
                    public void checkClientTrusted(X509Certificate[] x509Certificates, String s) throws CertificateException {
                    }

                    public void checkServerTrusted(X509Certificate[] x509Certificates, String s) throws CertificateException {
                    }

                    public X509Certificate[] getAcceptedIssuers() {
                        return null;
                    }
                }
        };
        SSLContext ctx = SSLContext.getInstance("TLS");
        ctx.init(null, trustManagers, null);
        connection.setSSLSocketFactory(ctx.getSocketFactory());
        // 获取文件流
        InputStream inStream = connection.getInputStream();
        // 保存到本地路径下
        FileOutputStream fs = new FileOutputStream(localPath);
        byte[] buffer = new byte[1024];
        while ((byteRead = inStream.read(buffer)) != -1) {
            fs.write(buffer, 0, byteRead);
        }
        inStream.close();
        fs.close();
    } catch (IOException | KeyManagementException | NoSuchAlgorithmException e) {
        e.printStackTrace();
    }
}
```

## 错误码<a name="section288814321256"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section4952152111818"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/record/downloadurls?confUUID=51adf610220411eaaae03f22d33cc26b'
```

