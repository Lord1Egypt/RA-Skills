# Legado 书源开发完整指南

> **版本**: 3.0  
> **更新时间**: 2026-03-13  
> **基于**: 40万行Legado源码分析 + 134个真实书源 + 完整知识库

---

## 📚 目录

1. [核心数据结构](#核心数据结构)
2. [规则语法详解](#规则语法详解)
3. [书源开发流程](#书源开发流程)
4. [常见陷阱与错误](#常见陷阱与错误)
5. [实战案例](#实战案例)
6. [调试技巧](#调试技巧)
7. [最佳实践](#最佳实践)
8. [书源配置开关详解](#书源配置开关详解)
9. [附录](#附录)

---

## 核心数据结构

### BookSource（书源主类）

```kotlin
data class BookSource(
    // 核心标识（必填）
    var bookSourceUrl: String = "",        // 书源地址（主键，唯一）
    var bookSourceName: String = "",       // 书源名称
    
    // 书源类型
    var bookSourceType: Int = 0,           // 0:文本, 1:音频, 2:图片, 3:文件, 4:视频
    var bookSourceGroup: String? = null,   // 书源分组
    
    // 状态控制
    var enabled: Boolean = true,           // 是否启用
    var enabledExplore: Boolean = true,    // 是否启用发现
    var customOrder: Int = 0,             // 手动排序编号
    
    // 性能指标
    var lastUpdateTime: Long = 0,          // 最后更新时间
    var respondTime: Long = 180000L,      // 响应时间（毫秒）
    var weight: Int = 0,                   // 智能排序权重
    
    // 请求配置
    var header: String? = null,           // 请求头（JSON格式）
    var enabledCookieJar: Boolean? = true, // 自动保存Cookie
    var concurrentRate: String? = null,   // 并发率限制
    
    // 规则配置（核心）
    var searchUrl: String? = null,         // 搜索URL模板
    var ruleSearch: SearchRule? = null,    // 搜索规则
    var ruleBookInfo: BookInfoRule? = null,// 书籍信息规则
    var ruleToc: TocRule? = null,          // 目录规则
    var ruleContent: ContentRule? = null,  // 正文规则
    var ruleExplore: ExploreRule? = null,  // 发现规则
    
    // 高级功能
    var jsLib: String? = null,             // JS库（可复用函数）
    var loginUrl: String? = null,          // 登录地址
    var loginUi: String? = null,           // 登录UI
    var loginCheckJs: String? = null,      // 登录检测JS
    var coverDecodeJs: String? = null,     // 封面解密JS
    var bookSourceComment: String? = null, // 注释
    var variableComment: String? = null,   // 自定义变量说明
    
    // 扩展功能
    var eventListener: Boolean = false,    // 是否监听事件
    var customButton: Boolean = false      // 自定义按钮
)
```

### SearchRule（搜索规则）

```kotlin
data class SearchRule(
    // 列表规则（必填）
    var bookList: String? = null,          // 书籍列表选择器
    
    // 字段提取规则
    var name: String? = null,              // 书名（必填）
    var author: String? = null,            // 作者
    var kind: String? = null,              // 分类
    var wordCount: String? = null,         // 字数
    var lastChapter: String? = null,       // 最新章节
    var intro: String? = null,             // 简介
    var coverUrl: String? = null,          // 封面URL
    var bookUrl: String? = null,           // 书籍URL（必填）
    
    // 验证规则
    var checkKeyWord: String? = null       // 校验关键词
)
```

### BookInfoRule（书籍信息规则）

```kotlin
data class BookInfoRule(
    // 初始化
    var init: String? = null,              // 初始化规则
    
    // 字段提取规则
    var name: String? = null,              // 书名（必填）
    var author: String? = null,            // 作者
    var intro: String? = null,             // 简介
    var kind: String? = null,              // 分类
    var lastChapter: String? = null,       // 最新章节
    var updateTime: String? = null,       // 更新时间
    var coverUrl: String? = null,          // 封面URL
    var tocUrl: String? = null,           // 目录URL
    var wordCount: String? = null,         // 字数
    
    // 扩展字段
    var canReName: String? = null,         // 可重命名
    var downloadUrls: String? = null       // 下载链接
)
```

### TocRule（目录规则）

```kotlin
data class TocRule(
    // 列表规则（必填）
    var chapterList: String? = null,      // 章节列表选择器
    
    // 字段提取规则（必填）
    var chapterName: String? = null,      // 章节名称
    var chapterUrl: String? = null,       // 章节URL
    
    // 分页和高级功能
    var nextTocUrl: String? = null,       // 目录下一页
    var preUpdateJs: String? = null,      // 更新前执行JS
    var formatJs: String? = null,          // 格式化JS
    
    // 章节标记
    var isVolume: String? = null,         // 是否卷
    var isVip: String? = null,            // 是否VIP
    var isPay: String? = null,            // 是否付费
    var updateTime: String? = null        // 更新时间
)
```

### ContentRule（正文规则）

```kotlin
data class ContentRule(
    // 内容规则（必填）
    var content: String? = null,          // 正文内容
    
    // 分页和导航
    var nextContentUrl: String? = null,   // 下一页URL（⚠️ 仅用于真正的下一章）
    var subContent: String? = null,       // 副文规则（拼接在正文后）
    var title: String? = null,            // 标题（有些网站只能在正文中获取）
    
    // 高级功能
    var webJs: String? = null,            // WebView注入JS
    var replaceRegex: String? = null,     // 替换规则
    var imageStyle: String? = null,       // 图片样式（默认/FULL）
    var imageDecode: String? = null,      // 图片解密JS
    var payAction: String? = null,        // 购买操作
    var callBackJs: String? = null       // 事件回调
)
```

---

## 规则语法详解

### 基本格式

```
选择器@提取类型##正则表达式##替换内容
```

**分隔符说明**：
- `@` - 分隔选择器和提取类型
- `##` - 分隔正则表达式
- 第二个 `##` 可省略（如果替换内容为空）

### 选择器类型

#### 1. 基础选择器

```css
/* 元素选择器 */
div@text
p@text
h1@text
a@href
img@src

/* 类选择器 */
.book-name@text
.author@text
.intro@text

/* ID选择器 */
#content@text
#main@html
```

#### 2. 属性选择器

```css
/* 存在属性 */
[href]@href
[class*=book]@text

/* 属性值匹配 */
[data-id="123"]@text
[href^="https://"]@href          /* 以https://开头 */
[href$=".html"]@href             /* 以.html结尾 */
[href*="book"]@href              /* 包含book */
```

#### 3. 组合选择器

```css
/* 后代选择器 */
.container .item@text
.book-list .book-name@text

/* 子元素选择器 */
ul > li@text
.book-info > h1@text

/* 相邻兄弟选择器 */
h1 + p@text
.title + .author@text

/* 通用兄弟选择器 */
.chapter ~ .notes@text
```

#### 4. ⚠️ 数字索引选择器（重要）

**正数索引**：
```css
.class.item.0@text    # 第一个
.class.item.1@text    # 第二个
.class.item.2@text    # 第三个
```

**负数索引**：
```css
.class.item.-1@text   # 倒数第一个
.class.item.-2@text   # 倒数第二个
.class.item.-3@text   # 倒数第三个
```

**排除索引**：
```css
.class.item.0!1@text      # 排除第1个
.class.item.0!1!2@text   # 排除第1和第2个
```

**区间索引**：
```css
.class.item.[0:5]@text     # 第0到第5个
.class.item.[1:3]@text     # 第1到第3个
.class.item.[0:-1]@text    # 第0到倒数第1个
```

**步长索引**：
```css
.class.item.[0:10:2]@text  # 第0到第10个，每2个取一个
.class.item.[0:10:3]@text  # 第0到第10个，每3个取一个
```

#### 5. 文本选择器（text.文本）

⚠️ **替代 `:contains()` 伪类选择器**

```css
text.下一章@href      # 提取包含"下一章"文本的元素的href
text.作者@text        # 提取包含"作者"文本的元素的文本
text.下一页@href      # 提取包含"下一页"文本的元素的href
```

### 提取类型详解

#### @text - 提取所有文本
- 提取元素及其所有子元素的文本内容
- 包含子元素的文本
- 适用场景：书名、作者、正文等纯文本提取

```css
.title@text      # 提取标题及其子元素的文本
.content@text    # 提取正文内容
```

#### @ownText - 只提取当前元素的文本
- 只提取当前元素的文本
- 不包含子元素
- 适用场景：需要排除子元素文本时

```css
.content@ownText    # 只提取当前div的文本
.author@ownText     # 只提取作者名（不包含子标签）
```

#### @html - 提取完整HTML结构
- 提取元素及其子元素的完整HTML
- 保留所有标签和属性
- 适用场景：保留格式、调试

```css
.content@html    # 提取包括p、span等标签的完整HTML
```

#### @textNode - 提取文本节点
- 提取所有文本节点
- 分段返回多个结果
- 适用场景：逐个处理文本节点

```css
.content@textNode    # 返回多个文本节点数组
```

#### @属性名 - 提取属性值
- 提取指定属性的值
- 常用属性：href、src、class、id、value、data-* 等

```css
a@href          # 提取链接地址
img@src         # 提取图片地址
img@data-original    # 提取懒加载图片地址
```

### 正则表达式

#### 基本格式

**格式1：删除匹配的内容**
```
选择器@提取类型##正则表达式
```
示例：`.author@text##^作者：` 删除"作者："前缀

**格式2：替换匹配的内容**
```
选择器@提取类型##正则表达式##替换内容
```
示例：`.price@text##\\$(\\d+)##￥$1` 将$替换为￥

**格式3：使用捕获组提取**
```
选择器@提取类型##正则表达式(捕获组)##$1
```
示例：`.author@text##.*作者：(.*)##$1` 提取"作者："后面的内容

#### 常用正则表达式

**清理前缀**：
```
##^作者：       # 删除开头的"作者："
##^《           # 删除开头的"《"
##^[^|]*\\|     # 删除第一个"|"及其前面的内容
```

**清理后缀**：
```
##（.*）$       # 删除括号及其内容
##》$          # 删除结尾的"》"
##\\s+$         # 删除结尾的空白
```

**提取特定内容**：
```
##.*作者：(.*)##$1      # 提取"作者："后面的内容
##第(\\d+)章##$1         # 提取章节号
##(\\d{4})-(\\d{2})-(\\d{2})##$1年$2月$3日  # 格式化日期
```

**清理广告和提示**：
```
##<div id="ad">[\\s\\S]*?</div>         # 删除广告div
##请收藏本站|本章完|继续阅读##         # 删除常见提示文本
##免费小说就上.*##                    # 删除网站推广文本
```

**多个清理规则**：
使用 `|` 分隔多个规则：
```
选择器@提取类型##规则1|规则2|规则3##
```

示例：
```json
{
  "content": "#chaptercontent@html##<div id=\"ad\">[\\s\\S]*?</div>|请收藏本站|本章完##"
}
```

### JS语法

#### 单行JS
```javascript
@js:let result = java.getString("$.title");
```

#### 多行JS
```javascript
<js>
let title = java.getString("$.title");
let author = java.getString("$.author");
result = title + " - " + author;
</js>
```

---

## 书源开发流程

### 阶段1：准备和分析

#### 1.1 检测编码
```bash
检测 https://www.example.com 的编码
```

**重要**：
- GBK网站必须配置 `"charset":"gbk"`
- UTF-8为默认编码，可省略

#### 1.2 分析搜索页
```bash
帮我分析 https://www.example.com 的搜索页结构
```

**获取信息**：
- 搜索URL格式
- 书籍列表容器选择器
- 书名、作者、封面等元素选择器
- 是否有懒加载图片
- 信息是否合并

#### 1.3 分析详情页
```bash
帮我分析 https://www.example.com 的详情页结构
```

**获取信息**：
- 书籍信息位置
- 目录链接
- 封面、作者、简介等

#### 1.4 分析目录页
```bash
帮我分析 https://www.example.com 的目录页结构
```

**获取信息**：
- 章节列表选择器
- 章节名称、URL
- 是否有分页

#### 1.5 分析正文页
```bash
帮我分析 https://www.example.com 的正文页结构
```

**获取信息**：
- 正文容器选择器
- 是否有"下一章"按钮
- 是否有广告需要清理
- 是否有分页

### 阶段2：配置规则

#### 2.1 配置searchUrl
```json
{
  "searchUrl": "/search?q={{key}}&page={{page}}"
}
```

**POST请求GBK编码**：
```json
{
  "searchUrl": "/search,{\"method\":\"POST\",\"body\":\"key={{key}}\",\"charset\":\"gbk\"}"
}
```

#### 2.2 配置ruleSearch
```json
{
  "ruleSearch": {
    "bookList": ".book-list .book-item",
    "name": ".title@text",
    "author": ".author@text",
    "coverUrl": "img@src",
    "bookUrl": "a@href"
  }
}
```

#### 2.3 配置ruleBookInfo
```json
{
  "ruleBookInfo": {
    "name": "h1@text",
    "author": ".author@text",
    "intro": ".intro@text",
    "coverUrl": ".cover@src",
    "tocUrl": ".toc-link@href"
  }
}
```

#### 2.4 配置ruleToc
```json
{
  "ruleToc": {
    "chapterList": "#chapter-list a",
    "chapterName": "text",
    "chapterUrl": "href"
  }
}
```

#### 2.5 配置ruleContent
```json
{
  "ruleContent": {
    "content": "#content@html##<div id=\"ad\">[\\s\\S]*?</div>##"
  }
}
```

### 阶段3：测试和调试

#### 3.1 测试搜索
1. 导入书源到Legado
2. 进行搜索测试
3. 查看搜索结果是否正确

#### 3.2 测试详情页
1. 点击书籍
2. 查看书名、作者、封面等信息
3. 验证规则是否正确提取

#### 3.3 测试目录
1. 进入目录
2. 查看章节列表
3. 验证章节顺序和链接

#### 3.4 测试正文
1. 进入章节阅读
2. 查看正文内容
3. 检查广告是否清理
4. 验证"下一章"功能

---

## 常见陷阱与错误

### 1. ❌ 字段错误

#### 错误：使用不存在的字段
```json
{
  "ruleContent": {
    "nextContentUrl": "text.下一章@href",
    "prevContentUrl": "text.上一章@href"  // ❌ 此字段不存在！
  }
}
```

**原因**：Legado源码中没有 `prevContentUrl` 字段

#### 错误：误用伪类选择器
```css
.name:first-child@text      // ❌ 不支持
.name:last-child@text       // ❌ 不支持
a:contains(下一章)@href    // ❌ 不支持
```

**正确**：
```css
.name.0@text                // ✅ 第一个
.name.-1@text               // ✅ 倒数第一个
text.下一章@href            // ✅ 文本选择器
```

### 2. ❌ @text vs @ownText 混淆

```html
<div class="author">
  作者：<span>张三</span>
</div>
```

**错误**：
```json
{
  "author": ".author@text"  // 提取"作者：张三"
}
```

**正确**：
```json
{
  "author": ".author@ownText"  // 只提取"作者："
}
```

### 3. ❌ 编码问题

**GBK网站未配置charset**：
```json
{
  "searchUrl": "/search.php?key={{key}}"  // ❌ GBK网站会出现乱码
}
```

**正确**：
```json
{
  "searchUrl": "/search.php,{\"method\":\"POST\",\"body\":\"key={{key}}\",\"charset\":\"gbk\"}"
}
```

### 4. ❌ nextContentUrl 误用

**场景1：分页场景**
```html
<!-- URL: /chapter/1.html?page=1 -->
<!-- 下一页: /chapter/1.html?page=2 -->
```

**错误**：
```json
{
  "ruleContent": {
    "nextContentUrl": "text.下一页@href"  // ❌ 这是分页，不是下一章
  }
}
```

**正确**：留空或不设置 `nextContentUrl`

**场景2：下一章场景**
```html
<!-- URL: /chapter/1.html -->
<!-- 下一章: /chapter/2.html -->
```

**正确**：
```json
{
  "ruleContent": {
    "nextContentUrl": "text.下一章@href"  // ✅ 这是真正的下一章
  }
}
```

### 5. ❌ 懒加载图片未处理

```html
<img class="lazy" data-original="http://example.com/cover.jpg" src="placeholder.jpg"/>
```

**错误**：
```json
{
  "coverUrl": "img@src"  // ❌ 提取到placeholder
}
```

**正确**：
```json
{
  "coverUrl": "img@data-original||img@src"  // ✅ 优先data-original
}
```

### 6. ❌ 正则表达式错误

**缺少分隔符**：
```json
{
  "author": ".author@text##^作者"  // ❌ 缺少结束符
}
```

**正确**：
```json
{
  "author": ".author@text##^作者：##"
}
```

**未处理边界情况**：
```json
{
  "name": "h1@text"  // 提取"《斗破苍穹》"
}
```

**正确**：
```json
{
  "name": "h1@text##^《|》$##"  // 提取"斗破苍穹"
}
```

### 7. ❌ POST请求配置错误

**method配置错误**：
```json
{
  "searchUrl": "/search,{\"body\":\"key={{key}}\"}"  // ❌ 缺少method
}
```

**正确**：
```json
{
  "searchUrl": "/search,{\"method\":\"POST\",\"body\":\"key={{key}}\"}"
}
```

**body格式错误**：
```json
{
  "searchUrl": "/search,{\"method\":\"POST\",\"body\":key={{key}}}"  // ❌ body应为JSON字符串
}
```

**正确**：
```json
{
  "searchUrl": "/search,{\"method\":\"POST\",\"body\":\"key={{key}}\"}"
}
```

### 8. ❌ JSONPath使用错误

**未以$.开头**：
```json
{
  "name": "data.title"  // ❌ 可能解析失败
}
```

**正确**：
```json
{
  "name": "$.data.title"  // ✅ 标准JSONPath
}
```

---

## 实战案例

### 案例1：标准小说站

**网站特征**：
- 完整的书籍信息（封面、作者、简介）
- 标准HTML结构
- UTF-8编码

**HTML结构**：
```html
<div class="book-list">
  <div class="book-item">
    <img src="cover.jpg" class="cover"/>
    <h3 class="title">斗破苍穹</h3>
    <p class="author">作者：天蚕土豆</p>
    <p class="intro">简介内容...</p>
    <a href="/book/1.html">详情</a>
  </div>
</div>
```

**书源配置**：
```json
{
  "bookSourceUrl": "https://www.example.com",
  "bookSourceName": "标准小说站",
  "bookSourceType": 0,
  "searchUrl": "/search?q={{key}}&page={{page}}",
  "ruleSearch": {
    "bookList": ".book-list .book-item",
    "name": ".title@text",
    "author": ".author@text",
    "coverUrl": ".cover@src",
    "intro": ".intro@text",
    "bookUrl": "a@href"
  },
  "ruleBookInfo": {
    "name": "h1@text",
    "author": ".author@text",
    "intro": ".intro@text",
    "coverUrl": ".cover@src",
    "tocUrl": ".toc-link@href"
  },
  "ruleToc": {
    "chapterList": "#chapter-list a",
    "chapterName": "text",
    "chapterUrl": "href"
  },
  "ruleContent": {
    "content": "#content@text"
  }
}
```

### 案例2：笔趣阁类（无封面，信息合并）

**网站特征**：
- 无封面图片
- 信息合并在一起
- 需要正则拆分

**HTML结构**：
```html
<div class="result-list">
  <div class="result-item">
    <h3><a href="/book/1">《斗破苍穹》</a></h3>
    <p class="info">科幻灵异 | 作者：天蚕土豆 | 更新：第100章</p>
  </div>
</div>
```

**书源配置**：
```json
{
  "bookSourceUrl": "https://www.bqge.com",
  "bookSourceName": "笔趣阁",
  "bookSourceType": 0,
  "searchUrl": "/search.php?q={{key}}",
  "ruleSearch": {
    "bookList": ".result-list .result-item",
    "name": "h3 a@text##^《|》$##",
    "author": ".info@text##.*作者：|\\|.*##",
    "kind": ".info@text##^.*\\| |\\|.*##",
    "lastChapter": ".info@text##.*更新：##",
    "bookUrl": "h3 a@href"
  },
  "ruleBookInfo": {
    "name": "h1@text##^《|》$##",
    "author": ".author@text##^作者：##",
    "intro": ".intro@text"
  },
  "ruleToc": {
    "chapterList": "#list dd a",
    "chapterName": "text",
    "chapterUrl": "href"
  },
  "ruleContent": {
    "content": "#content@text##免费小说就上.*|本章完##"
  }
}
```

### 案例3：POST请求GBK编码

**网站特征**：
- POST请求
- GBK编码
- 中文网站

**书源配置**：
```json
{
  "bookSourceUrl": "https://www.69shuba.com",
  "bookSourceName": "69书吧",
  "bookSourceType": 0,
  "searchUrl": "/modules/article/search.php,{\"method\":\"POST\",\"body\":\"searchkey={{key}}&searchtype=all\",\"charset\":\"gbk\"}",
  "ruleSearch": {
    "bookList": ".newbox li",
    "name": "a.0@text",
    "author": "span.-1@text##.*：##",
    "coverUrl": "img@src",
    "bookUrl": "a.0@href"
  },
  "ruleBookInfo": {
    "name": ".booknav2 h1@text",
    "author": ".booknav2 a.0@text",
    "intro": ".navtxt p.-1@text",
    "coverUrl": ".bookimg2 img@src"
  },
  "ruleToc": {
    "chapterList": "#catalog li",
    "chapterName": "a@text",
    "chapterUrl": "a@href"
  },
  "ruleContent": {
    "content": ".txtnav@html##<p>.*?</p>|<script[\\s\\S]*?</script>##"
  }
}
```

### 案例4：聚合源（JSON API）

**网站特征**：
- 返回JSON数据
- 使用JSONPath提取

**JSON响应**：
```json
{
  "code": 0,
  "data": {
    "records": [
      {
        "book_name": "斗破苍穹",
        "author": "天蚕土豆",
        "thumb_url": "http://example.com/cover.jpg",
        "abstract": "简介内容",
        "last_chapter": "第100章"
      }
    ]
  }
}
```

**书源配置**：
```json
{
  "bookSourceUrl": "https://api.example.com",
  "bookSourceName": "聚合源",
  "bookSourceType": 0,
  "searchUrl": "/api/search?keyword={{key}}&page={{page}}",
  "ruleSearch": {
    "bookList": "$.data.records[*]",
    "name": "$.book_name",
    "author": "$.author",
    "coverUrl": "$.thumb_url",
    "intro": "$.abstract",
    "lastChapter": "$.last_chapter",
    "bookUrl": "<js>...</js>"
  },
  "ruleBookInfo": {
    "name": "$.data.book_name",
    "author": "$.data.author",
    "intro": "$.data.abstract",
    "coverUrl": "$.data.thumb_url"
  },
  "ruleToc": {
    "chapterList": "$.data.chapters[*]",
    "chapterName": "$.title",
    "chapterUrl": "$.url"
  },
  "ruleContent": {
    "content": "$.data.content"
  }
}
```

---

## 调试技巧

### 1. 使用浏览器开发者工具

**步骤**：
1. 打开浏览器
2. 按F12打开开发者工具
3. 切换到Elements标签
4. 查看HTML结构
5. 测试CSS选择器

**测试选择器**：
```javascript
document.querySelector('.book-list')
document.querySelectorAll('.book-item')
document.querySelector('.title').textContent
```

### 2. 逐步验证规则

**验证顺序**：
1. 验证 bookList
2. 验证各个字段提取
3. 验证正则表达式
4. 验证完整流程

**方法**：
- 每次只验证一个规则
- 确认正确后再验证下一个
- 逐步缩小问题范围

### 3. 查看Legado调试日志

**步骤**：
1. 导入书源到Legado
2. 打开书源调试
3. 执行搜索/阅读
4. 查看详细日志

**查看内容**：
- 请求URL
- 响应内容
- 规则解析结果
- 错误信息

### 4. 使用@html调试

**用途**：查看HTML结构，调试选择器

**示例**：
```json
{
  "name": ".title@html"  // 返回完整HTML，查看结构
}
```

### 5. 常见问题排查

**搜索无结果**：
- 检查 bookList 是否正确
- 检查 searchUrl 格式
- 检查编码配置

**内容缺失**：
- 检查选择器是否匹配
- 检查是否动态加载
- 检查是否需要webView

**乱码问题**：
- 检查编码配置
- 确认网站编码类型
- 使用charset参数

---

## 最佳实践

### 1. 开发前准备

- ✅ 检测网站编码
- ✅ 分析HTML结构
- ✅ 使用真实HTML验证选择器
- ✅ 准备测试数据

### 2. 规则编写

- ✅ 优先使用类选择器 `.class-name`
- ✅ 使用ID选择器 `#id-name` 更精准
- ✅ 避免过深嵌套（最多3-4层）
- ✅ 使用数字索引 `.0`、`.-1` 替代伪类
- ✅ 合理使用正则清理广告
- ✅ 提取类型要准确（@text、@html、@ownText）

### 3. 特殊情况处理

- ✅ 懒加载：`img@data-original||img@src`
- ✅ 信息合并：使用正则拆分
- ✅ 动态加载：使用webView
- ✅ GBK编码：添加 `charset:"gbk"`
- ✅ POST请求：正确配置method和body

### 4. 测试验证

- ✅ 逐步验证每个规则
- ✅ 使用真实数据测试
- ✅ 检查边界情况
- ✅ 测试特殊字符
- ✅ 验证分页场景

### 5. 性能优化

- ✅ 避免不必要的规则
- ✅ 使用高效选择器
- ✅ 合理使用正则
- ✅ 减少网络请求

### 6. 代码规范

```json
{
  "bookSourceUrl": "https://www.example.com",
  "bookSourceName": "示例书源",
  "searchUrl": "/search?q={{key}}",
  "ruleSearch": {
    "bookList": ".book-list .book-item",
    "name": ".title@text",
    "author": ".author@text",
    "bookUrl": "a@href"
  }
}
```

---

## 书源配置开关详解

### 1. 启用/禁用功能

#### 1.1 `enabled` - 书源启用状态

**作用**：控制书源是否在阅读App中显示和使用

```json
{
  "enabled": true   // 启用书源（默认）
}
```

| 值 | 说明 | 使用场景 |
|----|------|----------|
| `true` | 启用书源 | 正常使用的书源 |
| `false` | 禁用书源 | 临时关闭、维护中的书源 |

**⚠️ 注意**：
- 禁用后，该书源不会参与任何搜索和阅读操作
- 仍可在书源管理界面查看和编辑
- 用户也可以在App中手动禁用书源

#### 1.2 `enabledExplore` - 发现页启用

**作用**：控制书源是否出现在发现页推荐中

```json
{
  "enabledExplore": true   // 启用发现（默认）
}
```

| 值 | 说明 | 使用场景 |
|----|------|----------|
| `true` | 显示在发现页 | 正常推广的书源 |
| `false` | 不显示在发现页 | 测试中、仅搜索使用的书源 |

**使用场景**：
- 只用于搜索的书源：`enabledExplore: false`
- 仅供内部使用的测试源：`enabledExplore: false`
- 正式发布的优质源：`enabledExplore: true`

---

### 2. Cookie 功能

#### 2.1 `enabledCookieJar` - Cookie 自动保存

**作用**：控制是否自动保存网站返回的Cookie，下次请求时自动携带

```json
{
  "enabledCookieJar": true   // 自动保存Cookie（默认）
}
```

| 值 | 说明 | 使用场景 |
|----|------|----------|
| `true` | 自动保存Cookie | 需要登录状态、会话保持 |
| `false` | 不保存Cookie | 静态网站、每次独立请求 |

**✅ 需要开启的场景**：
- 需要登录才能访问的网站
- 有阅读限制的VIP内容
- 需要保持会话状态
- 反爬虫需要Cookie验证

**❌ 不需要开启的场景**：
- 完全公开的静态网站
- 每次请求独立、无状态
- Cookie会过期导致频繁失效

**⚠️ 注意**：
- Cookie保存在本地App中，不会自动清除
- 某些网站Cookie有效期很短，需要频繁刷新
- 敏感网站注意Cookie隐私问题

---

### 3. 请求头配置

#### 3.1 `header` - 自定义请求头

**作用**：自定义HTTP请求头，模拟浏览器、添加认证等

```json
{
  "header": "{\"User-Agent\":\"Mozilla/5.0...\",\"Referer\":\"https://example.com\"}"
}
```

**常用请求头**：

| 请求头 | 说明 | 示例 |
|--------|------|------|
| `User-Agent` | 浏览器标识 | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."` |
| `Referer` | 来源页面 | `"https://www.example.com"` |
| `Cookie` | Cookie字符串 | `"session_id=xxx; token=yyy"` |
| `Authorization` | 认证信息 | `"Bearer xxx"` |
| `X-Requested-With` | AJAX标识 | `"XMLHttpRequest"` |

**完整示例**：
```json
{
  "header": "{\n  \"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\",\n  \"Referer\": \"https://www.example.com\",\n  \"Accept\": \"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\",\n  \"Accept-Language\": \"zh-CN,zh;q=0.9\"\n}"
}
```

**⚠️ 注意**：
- `header` 字段必须是JSON字符串格式
- 与 `enabledCookieJar` 配合使用：`enabledCookieJar` 控制Cookie自动保存，`header` 手动设置Cookie
- 如果网站检测到反爬虫，可能需要设置多个请求头

---

### 4. 登录功能

#### 4.1 `loginUrl` - 登录地址

**作用**：设置登录页面URL，用户可手动登录保存Cookie

```json
{
  "loginUrl": "https://www.example.com/login"
}
```

**使用场景**：
- 需要登录才能访问的VIP内容
- 有会员限制的网站
- 需要账号才能使用的书源

#### 4.2 `loginUi` - 登录界面配置

**作用**：自定义登录表单界面

```json
{
  "loginUi": "<form>\n  <input name=\"username\" label=\"用户名\"/>\n  <input name=\"password\" type=\"password\" label=\"密码\"/>\n</form>"
}
```

#### 4.3 `loginCheckJs` - 登录检测脚本

**作用**：使用JS检测登录状态

```json
{
  "loginCheckJs": "result.match(/退出|用户中心/)!=null"
}
```

**使用场景**：
- 自动检测登录是否成功
- 动态判断是否需要重新登录
- 检测VIP状态

**⚠️ 注意**：
- `loginCheckJs` 应返回 `true`（已登录）或 `false`（未登录）
- 结果保存在 `result` 变量中

---

### 5. 高级功能开关

#### 5.1 `eventListener` - 事件监听

**作用**：是否启用WebView事件监听（用于复杂交互）

```json
{
  "eventListener": false   // 默认关闭
}
```

| 值 | 说明 | 使用场景 |
|----|------|----------|
| `true` | 启用事件监听 | 需要监听页面事件、点击操作 |
| `false` | 关闭事件监听 | 普通静态页面 |

**使用场景**：
- 需要等待页面加载完成
- 需要监听特定元素点击
- 需要与页面交互获取数据

#### 5.2 `customButton` - 自定义按钮

**作用**：是否启用自定义按钮功能

```json
{
  "customButton": false   // 默认关闭
}
```

**使用场景**：
- 需要在阅读界面添加自定义按钮
- 需要额外操作（如签到、投票等）

---

### 6. 编码配置

#### 6.1 `charset` - 字符集设置

**作用**：指定请求/响应的字符编码，解决中文乱码问题

**位置**：在 `searchUrl` 或具体请求的配置JSON中

```json
{
  "searchUrl": "/search?q={{key}},{\"charset\":\"gbk\"}"
}
```

| 编码 | 说明 | 使用场景 |
|------|------|----------|
| `"gbk"` | GBK编码 | 老式中文网站、部分小说站 |
| `"utf-8"` | UTF-8编码 | 现代网站（默认） |
| `"big5"` | BIG5编码 | 繁体中文网站 |

**⚠️ 注意**：
- GBK网站必须设置 `charset:"gbk"`，否则会出现乱码
- URL中的中文参数需要特殊处理：`java.encodeURI(key, 'GBK')`

**完整示例**：
```json
{
  "searchUrl": "/search.php?key={{java.encodeURI(key, 'GBK')}}&page={{page}},\"method\":\"POST\",\"body\":\"key={{java.encodeURI(key, 'GBK')}}\",\"charset\":\"gbk\"}"
}
```

---

### 7. 并发控制

#### 7.1 `concurrentRate` - 并发率限制

**作用**：限制并发请求数，防止触发网站反爬虫

```json
{
  "concurrentRate": "3"   // 最多3个并发请求
}
```

**使用场景**：
- 反爬虫严格的网站
- 服务器响应较慢的网站
- 需要控制请求频率

**⚠️ 注意**：
- 并发率过高可能导致IP被封禁
- 并发率过低会降低加载速度
- 建议根据网站实际情况调整（默认3-5）

---

### 8. 图片处理

#### 8.1 `imageStyle` - 图片样式

**作用**：控制图片的显示方式

```json
{
  "ruleContent": {
    "imageStyle": "FULL"   // 图片全宽显示
  }
}
```

| 值 | 说明 | 使用场景 |
|----|------|----------|
| `"FULL"` | 全宽显示 | 漫画、大图 |
| 未设置（默认） | 原始大小 | 普通插图 |

#### 8.2 `imageDecode` - 图片解密JS

**作用**：对加密图片进行解密处理

```json
{
  "ruleContent": {
    "imageDecode": "baseUrl+'?token='+result"
  }
}
```

**使用场景**：
- 图片URL需要添加token
- 图片有防盗链处理
- 图片需要特殊请求参数

#### 8.3 `coverDecodeJs` - 封面解密JS

**作用**：对封面图片进行解密处理（与imageDecode类似）

```json
{
  "coverDecodeJs": "result.replace(/^http:/, 'https:')"
}
```

---

### 9. 性能指标

#### 9.1 `respondTime` - 响应时间

**作用**：设置请求超时时间（毫秒）

```json
{
  "respondTime": 180000   // 180秒超时（默认）
}
```

**使用场景**：
- 网站响应较慢时增加超时时间
- 快速网站可缩短超时时间
- 避免长时间等待

#### 9.2 `weight` - 智能排序权重

**作用**：控制书源在搜索结果中的排序优先级

```json
{
  "weight": 10   // 权重越高，排序越靠前
}
```

**使用场景**：
- 优质源设置高权重（如10-20）
- 普通源默认权重（0）
- 测试源设置低权重（如-10）

---

### 10. 注释和文档

#### 10.1 `bookSourceComment` - 书源注释

**作用**：添加书源的说明、版本、作者等信息

```json
{
  "bookSourceComment": "版本: v1.2\\n作者: xxx\\n更新: 2026-03-13\\n说明: 这是一个优质小说站"
}
```

**建议内容**：
- 版本号
- 作者/维护者
- 更新日期
- 功能说明
- 已知问题

#### 10.2 `variableComment` - 变量注释

**作用**：说明自定义变量的用途

```json
{
  "variableComment": "{\\n  \"token\": \"API令牌\\n\",\\n  \"uid\": \"用户ID\\n\"}"
}
```

---

### 配置开关速查表

| 配置项 | 类型 | 默认值 | 作用 | 常见场景 |
|--------|------|--------|------|----------|
| `enabled` | Boolean | `true` | 启用书源 | 临时关闭书源 |
| `enabledExplore` | Boolean | `true` | 发现页显示 | 测试源不显示 |
| `enabledCookieJar` | Boolean | `true` | 自动保存Cookie | 需要登录、会话保持 |
| `header` | String | `null` | 自定义请求头 | 反爬虫、认证 |
| `loginUrl` | String | `null` | 登录地址 | VIP内容 |
| `loginCheckJs` | String | `null` | 登录检测 | 自动检测登录状态 |
| `eventListener` | Boolean | `false` | 事件监听 | 复杂交互页面 |
| `charset` | String | `"utf-8"` | 字符编码 | GBK网站 |
| `concurrentRate` | String | `null` | 并发率 | 反爬虫限制 |
| `respondTime` | Long | `180000` | 超时时间 | 响应慢的网站 |
| `weight` | Int | `0` | 排序权重 | 优质源优先 |
| `imageStyle` | String | 默认 | 图片样式 | 漫画全宽显示 |
| `imageDecode` | String | `null` | 图片解密 | 加密图片 |
| `bookSourceComment` | String | `null` | 书源注释 | 版本、作者信息 |

---

### 常见配置场景

#### 场景1：普通静态网站

```json
{
  "enabled": true,
  "enabledExplore": true,
  "enabledCookieJar": false
}
```

#### 场景2：需要登录的VIP网站

```json
{
  "enabled": true,
  "enabledExplore": false,
  "enabledCookieJar": true,
  "loginUrl": "https://www.example.com/login",
  "loginCheckJs": "result.match(/退出/)!=null",
  "header": "{\"Cookie\":\"session_id=xxx\"}"
}
```

#### 场景3：GBK编码的老式小说站

```json
{
  "searchUrl": "/search.php?key={{java.encodeURI(key, 'GBK')}}&page={{page}},{\"charset\":\"gbk\"}",
  "enabledCookieJar": true
}
```

#### 场景4：反爬虫严格的网站

```json
{
  "concurrentRate": "2",
  "respondTime": 60000,
  "header": "{\n  \"User-Agent\": \"Mozilla/5.0...\",\n  \"Referer\": \"https://www.example.com\"\n}",
  "enabledCookieJar": true
}
```

#### 场景5：漫画书源

```json
{
  "bookSourceType": 2,
  "ruleContent": {
    "imageStyle": "FULL",
    "imageDecode": "baseUrl+'?token='+result"
  }
}
```

---

## 附录

### 常用选择器速查

| 选择器 | 说明 | 示例 |
|--------|------|------|
| `.class` | 类选择器 | `.title@text` |
| `#id` | ID选择器 | `#content@text` |
| `element` | 元素选择器 | `div@text` |
| `[attr]` | 属性选择器 | `[href]@href` |
| `[attr=val]` | 属性值选择器 | `[class="book"]@text` |
| `parent child` | 后代选择器 | `.book-list .book-item` |
| `parent > child` | 子元素选择器 | `ul > li` |
| `.class.0` | 第一个 | `.item.0@text` |
| `.class.-1` | 倒数第一个 | `.item.-1@text` |
| `text.文本` | 文本选择器 | `text.下一章@href` |

### 提取类型速查

| 类型 | 说明 | 示例 |
|------|------|------|
| `@text` | 所有文本 | `.content@text` |
| `@ownText` | 元素自身文本 | `.content@ownText` |
| `@html` | 完整HTML | `.content@html` |
| `@href` | 链接地址 | `a@href` |
| `@src` | 图片地址 | `img@src` |
| `@textNode` | 文本节点 | `.content@textNode` |

### 常用正则速查

| 正则 | 说明 | 示例 |
|------|------|------|
| `^` | 行首 | `^作者：##` |
| `$` | 行尾 | `》$##` |
| `.*` | 任意字符 | `##.*##` |
| `.*?` | 非贪婪 | `##.*?##` |
| `(.*?)` | 捕获组 | `##(.*?)##$1` |
| `\\d` | 数字 | `##\\d##` |
| `\\s` | 空白 | `##\\s##` |
| `|` | 或 | `规则1|规则2` |

---

*本指南基于40万行Legado源码分析、134个真实书源和完整知识库整理而成*
