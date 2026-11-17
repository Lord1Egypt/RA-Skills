# Layouts

从 [assets/template.html](../assets/template.html) 拷贝后，用下面骨架替换 `<!-- SLIDES_START -->` 与 `<!-- SLIDES_END -->` 之间的内容。  
只改括号里的文案，不要改 class 层级。

## L1 封面

```html
<section class="slide" data-title="封面">
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div class="kicker">ENGLISH KICKER · Topic</div>
    <h1>中文主标题</h1>
    <p class="sub" style="font-size:22px;color:var(--ink2)">副标题第一句。<br>副标题第二句。</p>
    <div style="display:flex;gap:10px;margin-top:10px">
      <span class="tag">标签一</span><span class="tag">标签二</span><span class="tag">标签三</span>
    </div>
  </div>
  <div class="foot"><span>场合 · 日期</span><span>→ 或空格 翻页 · N 讲稿 · R 重放动画 · F 全屏</span></div>
  <aside class="notes">开场讲稿。</aside>
</section>
```

## L2 双栏讲解

```html
<section class="slide" data-title="要点">
  <div class="kicker">01 · 章节</div>
  <h2>一句结论当标题</h2>
  <p class="sub">一层解释，不要第二段。</p>
  <div class="row">
    <div class="col">
      <ul class="pts">
        <li><span class="n">1</span><span><b>要点一：</b>判断 + 短证据。</span></li>
        <li><span class="n">2</span><span><b>要点二：</b>判断 + 短证据。</span></li>
        <li><span class="n">3</span><span><b>要点三：</b>判断 + 短证据。</span></li>
      </ul>
    </div>
    <div class="col">
      <div class="panel" style="flex:1">
        <h3>右侧标题</h3>
        <p class="small">证据、示意或约束。</p>
      </div>
      <div class="callout">一句话结论。</div>
    </div>
  </div>
  <aside class="notes">本页讲稿。</aside>
</section>
```

需要终端时，把左侧换成 L3 的 `.term`；需要图谱时，右侧用 [components.md](components.md) 的 `.mg` 片段。

## L3 终端页

```html
<section class="slide" data-title="终端">
  <div class="kicker">02 · 章节</div>
  <h2>一句结论当标题</h2>
  <div class="row" style="margin-top:8px">
    <div class="col">
      <div class="term" style="flex:1">
        <span class="fname">path/file.md</span>
        <div class="body" style="margin-top:22px">
          <span class="h1">标题</span><span class="hr"></span>
          正文。<span class="lk">链接词</span> 和 <span class="em">强调</span>。
          <span class="cm">—— 注释</span>
        </div>
      </div>
    </div>
    <div class="col">
      <ul class="pts">
        <li><span class="n">1</span><span><b>解释一：</b>对应终端里的内容。</span></li>
        <li><span class="n">2</span><span><b>解释二：</b>对应终端里的内容。</span></li>
      </ul>
      <div class="callout teal">一句话结论。</div>
    </div>
  </div>
  <aside class="notes">本页讲稿。</aside>
</section>
```

## L4 目录树

```html
<section class="slide" data-title="目录">
  <div class="kicker">03 · 章节</div>
  <h2>三层结构 + 一句话协议</h2>
  <div class="row" style="margin-top:6px">
    <div class="col" style="flex:.95">
      <div class="panel tight" style="flex:1">
        <div class="small" style="margin-bottom:6px">目录名
          <span class="tag raw" style="margin-left:8px">输入</span>
          <span class="tag wiki">处理</span>
          <span class="tag out">输出</span>
        </div>
        <div class="ftree">
          <div class="fr root"><span class="con"></span><svg class="ic root"><use href="#i-folder"/></svg><span class="nm">root/</span><span class="desc">根目录</span></div>
          <div class="fr"><span class="con">├─</span><svg class="ic file"><use href="#i-file"/></svg><span class="nm hl">RULES.md</span><span class="desc">协议</span></div>
          <div class="fr"><span class="con">├─</span><svg class="ic folder"><use href="#i-folder"/></svg><span class="nm rawc">input/</span><span class="desc">原料</span></div>
          <div class="fr"><span class="con">├─</span><svg class="ic folder"><use href="#i-folder"/></svg><span class="nm wikic">work/</span><span class="desc">加工结果</span><span class="cnt">12</span></div>
          <div class="fr"><span class="con">└─</span><svg class="ic folder"><use href="#i-folder"/></svg><span class="nm outc">output/</span><span class="desc">交付物</span></div>
        </div>
      </div>
    </div>
    <div class="col">
      <div class="panel" style="flex:1;display:flex;flex-direction:column;gap:10px">
        <h3>协议怎么生效</h3>
        <div class="chip on load"><span class="k">① 启动</span>先读规则</div>
        <ul class="rules">
          <li class="on">规则一</li>
          <li class="on">规则二</li>
          <li class="on">规则三</li>
          <li class="on">规则四</li>
        </ul>
        <div class="chip on"><span class="k">② 动手</span>按规则执行</div>
      </div>
    </div>
  </div>
  <aside class="notes">本页讲稿。</aside>
</section>
```

## L5 对话卡

```html
<section class="slide" data-title="对话">
  <div class="kicker">04 · 章节</div>
  <h2>人说人话，系统回步骤</h2>
  <div class="row" style="margin-top:8px">
    <div class="col" style="flex:1.15;gap:10px">
      <div class="pcard on"><div class="u">用户原话。</div><div class="a">系统回：步骤一 → 步骤二 → 结果。</div></div>
      <div class="pcard on"><div class="u">用户原话。</div><div class="a">系统回：步骤一 → 步骤二 → 结果。</div></div>
    </div>
    <div class="col">
      <div class="panel">
        <h3>协作节拍</h3>
        <ol class="steps v" style="flex-direction:column;gap:6px">
          <li><b>第一步</b>说明。</li>
          <li><b>第二步</b>说明。</li>
          <li><b>第三步</b>说明。</li>
        </ol>
      </div>
      <div class="callout teal">一句话结论。</div>
    </div>
  </div>
  <aside class="notes">本页讲稿。</aside>
</section>
```

## L6 术语卡

```html
<section class="slide" data-title="术语">
  <div class="kicker">05 · 章节</div>
  <h2>先统一叫法，再往下讲</h2>
  <p class="sub">每个词只解释一件事。</p>
  <div class="row">
    <div class="col">
      <div class="glossary">
        <div class="g"><b>term-a</b>一句话定义。</div>
        <div class="g"><b>term-b</b>一句话定义。</div>
        <div class="g"><b>term-c</b>一句话定义。</div>
        <div class="g"><b>term-d</b>一句话定义。</div>
      </div>
    </div>
    <div class="col">
      <div class="callout">这三个词够用。其它同义词并进术语表，不要并列发明。</div>
    </div>
  </div>
  <aside class="notes">本页讲稿。</aside>
</section>
```

## L7 步骤条

```html
<section class="slide" data-title="步骤">
  <div class="kicker">06 · 章节</div>
  <h2>五步做完，全程说人话</h2>
  <div class="row" style="margin-top:8px">
    <div class="col">
      <ol class="steps v" style="flex-direction:column;gap:8px">
        <li><b>第一步</b>说明。</li>
        <li><b>第二步</b>说明。</li>
        <li><b>第三步</b>说明。</li>
        <li><b>第四步</b>说明。</li>
        <li><b>第五步</b>说明。</li>
      </ol>
    </div>
    <div class="col">
      <div class="panel" style="flex:1">
        <h3>配套材料</h3>
        <p class="small">提示词、检查项或注意点。</p>
      </div>
      <div class="callout">关键提醒只留一条。</div>
    </div>
  </div>
  <aside class="notes">本页讲稿。</aside>
</section>
```

横排三步用：

```html
<ol class="steps">
  <li><b>建结构</b>说明。</li>
  <li><b>填内容</b>说明。</li>
  <li><b>跑校验</b>说明。</li>
</ol>
```

## L8 对比收束

```html
<section class="slide" data-title="总结">
  <div class="kicker">回顾</div>
  <h2>人负责判断，系统负责执行</h2>
  <div class="two" style="margin-top:10px">
    <div class="who" style="border-color:rgba(245,181,68,.5)"><h4 style="color:var(--amber)">人做的事</h4><ul><li>事项一</li><li>事项二</li><li>事项三</li></ul></div>
    <div class="who" style="border-color:rgba(61,214,192,.5)"><h4 style="color:var(--teal)">系统做的事</h4><ul><li>事项一</li><li>事项二</li><li>事项三</li></ul></div>
  </div>
  <div style="margin-top:22px">
    <h3>今天就能开始的三步</h3>
    <ol class="steps">
      <li><b>第一步</b>说明。</li>
      <li><b>第二步</b>说明。</li>
      <li><b>第三步</b>说明。</li>
    </ol>
  </div>
  <div class="foot"><span>参考 / 来源</span><span>Q &amp; A</span></div>
  <aside class="notes">收束讲稿。</aside>
</section>
```

## 选页规则

- 第 1 页必须是 L1。
- 最后一页优先 L8。
- 中间页在 L2–L7 间轮换，连续 3 页不要同一结构。
- 需要「工作日志 / 树图点亮 / 进度条」时，先用 L2/L3 静态版；用户明确要重放，再加 [animations.md](animations.md)。
