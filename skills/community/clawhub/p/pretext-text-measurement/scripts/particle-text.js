#!/usr/bin/env node
/**
 * particle-text.js — 文字粒子自由运动引擎
 * 用法：
 *   node scripts/particle-text.js --text "你好" [选项...]
 *   node scripts/particle-text.js --text "你好" --output info
 */

const path = require('path');
const fs = require('fs');
const SKILL_DIR = path.resolve(__dirname, '..');

function unicodeCharWidth(code) {
  if (code >= 0x4E00 && code <= 0x9FFF) return 1.0;
  if (code >= 0x3400 && code <= 0x4DBF) return 1.0;
  if (code >= 0x20000 && code <= 0x2A6DF) return 1.0;
  if (code >= 0xAC00 && code <= 0xD7AF) return 1.0;
  if (code >= 0x3040 && code <= 0x309F) return 1.0;
  if (code >= 0x30A0 && code <= 0x30FF) return 1.0;
  if (code >= 0xFF00 && code <= 0xFFEF) return 1.0;
  if (code >= 0x1F300 && code <= 0x1F9FF) return 1.5;
  if (code >= 0x1FA00 && code <= 0x1FAD6) return 1.5;
  if (code === 0x200D || code === 0xFE0F || code === 0xFE0E) return 0;
  if (code >= 0x1F1E6 && code <= 0x1F1FF) return 0.8;
  if (code === 0x2014 || code === 0x2013) return 0.35;
  if (code === 0x0020 || code === 0x00A0) return 0.25;
  if (code === 0x0009) return 2.0;
  if (code === 0x000A || code === 0x000D) return 0;
  if (code >= 0x0041 && code <= 0x005A) return 0.7;
  if (code >= 0x0061 && code <= 0x007A) return 0.55;
  if (code >= 0x0030 && code <= 0x0039) return 0.55;
  return 0.55;
}

function estimateWidth(text, fontSize) {
  let w = 0;
  for (const ch of text) w += unicodeCharWidth(ch.codePointAt(0));
  return w * fontSize;
}

function wrapLines(text, maxWidth, fontSize) {
  const lines = [];
  for (const ch of text) {
    const w = estimateWidth(ch, fontSize);
    if (lines.length === 0 || estimateWidth(lines[lines.length - 1] + ch, fontSize) > maxWidth) {
      lines.push(ch);
    } else {
      lines[lines.length - 1] += ch;
    }
  }
  return lines;
}

function seededRandom(seed) {
  let s = seed;
  return function() {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

function parseFontSize(font) {
  const m = font.match(/(\d+(?:\.\d+)?)\s*px/i);
  return m ? parseFloat(m[1]) : 32;
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function generateDemoHTML(opts) {
  const text = opts.text || '你好，世界！Hello World!';
  const fontSize = opts.fontSize || parseFontSize(opts.font || '32px sans-serif');
  const lineHeight = fontSize * 1.8;
  const W = opts.canvasWidth || 800;
  const H = opts.canvasHeight || 500;
  const bgColor = opts.bgColor || '#0a0a1a';
  const particleColor = opts.particleColor || '#FFD93D';
  const wrapMode = opts.wrapMode || 'bounce';
  const seed = 42;

  const rng = seededRandom(seed);
  const lines = wrapLines(text, W - 40, fontSize);
  const particles = [];
  const startY = (H - lines.length * lineHeight) / 2;
  lines.forEach(function(line, li) {
    const lineW = estimateWidth(line, fontSize);
    let x = (W - lineW) / 2;
    for (const ch of line) {
      const chW = unicodeCharWidth(ch.codePointAt(0)) * fontSize;
      particles.push({
        char: ch,
        x: x + (rng() - 0.5) * 50,
        y: startY + li * lineHeight + (rng() - 0.5) * 30,
        vx: (rng() - 0.5) * 0.3,
        vy: (rng() - 0.5) * 0.3,
        w: chW
      });
      x += chW;
    }
  });

  // 构建 HTML（不用模板字符串，全程字符串拼接）
  var palette = ['#FFD93D','#FF6B9D','#6BCB77','#4D96FF','#C77DFF','#FF9A3C','#00D4FF'];
  var particlesJson = JSON.stringify(particles);

  var html = '<!DOCTYPE html>\n';
  html += '<html lang="zh">\n<head>\n';
  html += '<meta charset="UTF-8">\n';
  html += '<meta name="viewport" content="width=device-width,initial-scale=1">\n';
  html += '<title>Pretext 文字粒子自由运动</title>\n';
  html += '<style>\n';
  html += '*{box-sizing:border-box;margin:0;padding:0}\n';
  html += 'body{display:flex;flex-direction:column;align-items:center;';
  html += 'justify-content:center;min-height:100vh;background:' + bgColor + ';';
  html += 'font-family:system-ui,sans-serif;overflow:hidden}\n';
  html += 'canvas{display:block;cursor:crosshair;border-radius:16px;';
  html += 'box-shadow:0 20px 80px rgba(0,0,0,0.5)}\n';
  html += '.controls{position:fixed;bottom:1.5rem;display:flex;gap:0.75rem;';
  html += 'flex-wrap:wrap;justify-content:center;padding:0 1rem}\n';
  html += '.btn{background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.7);';
  html += 'border:1px solid rgba(255,255,255,0.15);padding:0.5rem 1.2rem;';
  html += 'border-radius:50px;font-size:0.82rem;cursor:pointer;';
  html += 'transition:all 0.2s;backdrop-filter:blur(8px)}\n';
  html += '.btn:hover{background:rgba(255,255,255,0.15);color:#fff}\n';
  html += '.btn.on{background:' + particleColor + ';color:' + bgColor + ';font-weight:700}\n';
  html += '.info{position:fixed;top:1rem;left:1rem;color:rgba(255,255,255,0.4);';
  html += 'font-size:0.72rem;line-height:1.6;pointer-events:none}\n';
  html += '.info strong{color:' + particleColor + '}\n';
  html += 'h1{color:' + particleColor + ';font-size:1.1rem;margin-bottom:0.5rem;';
  html += 'font-family:system-ui,sans-serif}\n';
  html += '</style>\n';
  html += '</head>\n<body>\n';
  html += '<div class="info">\n';
  html += '<strong>Pretext 粒子引擎</strong><br>\n';
  html += '<span id="pc"></span>\n';
  html += '<span id="fps"></span>\n';
  html += '<span id="wm"></span>\n';
  html += '<span id="ms"></span>\n';
  html += '</div>\n';
  html += '<canvas id="c" width="' + W + '" height="' + H + '"></canvas>\n';
  html += '<div class="controls">\n';
  html += '<button class="btn" id="b1" onclick="setW(\'bounce\',this)">反弹</button>\n';
  html += '<button class="btn" id="b2" onclick="setW(\'wrap\',this)">环绕</button>\n';
  html += '<button class="btn" id="bg" onclick="tgG(this)">重力</button>\n';
  html += '<button class="btn" onclick="exp()">爆炸</button>\n';
  html += '<button class="btn" onclick="rst()">重置</button>\n';
  html += '<button class="btn" id="bt" onclick="tgT(this)">打字机</button>\n';
  html += '</div>\n';
  html += '<script>\n';

  // JS 逻辑（全程不用 Unicode 引号字符）
  html += 'var pts=' + particlesJson + ';\n';
  html += 'var FS=' + fontSize + ',LH=' + lineHeight + ',FR=0.98,MR=120,MF=8;\n';
  html += 'var cv=document.getElementById("c"),ctx=cv.getContext("2d");\n';
  html += 'var W=' + W + ',H=' + H + ',mx=W/2,my=H/2,ma=false;\n';
  html += 'var wm="' + wrapMode + '",gr=false,ti=false,tidx=0,lk=performance.now();\n';
  html += 'var pal=' + JSON.stringify(palette) + ';\n';
  html += 'var INIT=JSON.parse(JSON.stringify(pts));\n';

  // 鼠标事件
  html += 'cv.addEventListener("mousemove",function(e){var r=cv.getBoundingClientRect();';
  html += 'mx=(e.clientX-r.left)*(W/r.width);my=(e.clientY-r.top)*(H/r.height);';
  html += 'ma=true;document.getElementById("ms").textContent=" \u6d3e\u6d3e"});';
  html += 'cv.addEventListener("mouseleave",function(){ma=false;';
  html += 'document.getElementById("ms").textContent=" \u7a7a\u95f2"});';
  html += 'cv.addEventListener("click",function(e){var r=cv.getBoundingClientRect();';
  html += 'var cx=(e.clientX-r.left)*(W/r.width),cy=(e.clientY-r.top)*(H/r.height);';
  html += 'pts.forEach(function(p){var dx=p.x+p.w/2-cx,dy=p.y+FS/2-cy,';
  html += 'd=Math.sqrt(dx*dx+dy*dy);';
  html += 'if(d<150&&d>0){var f=(150-d)/150*12;p.vx+=(dx/d)*f;p.vy+=(dy/d)*f}})});';

  // update
  html += 'function upd(){var vc=ti?Math.min(Math.floor(tidx),pts.length):pts.length;';
  html += 'for(var i=0;i<vc;i++){var p=pts[i];if(!p)continue;';
  html += 'if(ma){var dx=p.x+p.w/2-mx,dy=p.y+FS/2-my,d=Math.sqrt(dx*dx+dy*dy);';
  html += 'if(d<MR&&d>0){var f=(MR-d)/MR*MF;p.vx+=(dx/d)*f;p.vy+=(dy/d)*f}}';
  html += 'if(gr)p.vy+=0.025;p.vx*=FR;p.vy*=FR;';
  html += 'p.vx+=(Math.random()-0.5)*0.04;p.vy+=(Math.random()-0.5)*0.02;';
  html += 'var sp=Math.sqrt(p.vx*p.vx+p.vy*p.vy);';
  html += 'if(sp>4){p.vx=(p.vx/sp)*4;p.vy=(p.vy/sp)*4}';
  html += 'p.x+=p.vx;p.y+=p.vy;';
  html += 'if(wm==="bounce"){';
  html += 'if(p.x<0){p.x=0;p.vx*=-0.7}';
  html += 'if(p.x+p.w>W){p.x=W-p.w;p.vx*=-0.7}';
  html += 'if(p.y<0){p.y=0;p.vy*=-0.7}';
  html += 'if(p.y+FS>H){p.y=H-FS;p.vy*=-0.7}}';
  html += 'else{if(p.x+p.w<0)p.x=W;if(p.x>W)p.x=-p.w;';
  html += 'if(p.y+FS<0)p.y=H;if(p.y>H)p.y=-FS}}}';
  html += 'if(ti)tidx=Math.min(tidx+0.8,pts.length)}';

  // draw
  html += 'function drw(){ctx.clearRect(0,0,W,H);';
  html += 'var g=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)/1.5);';
  html += "g.addColorStop(0,'" + bgColor + "');";
  html += 'g.addColorStop(1,"#050510");ctx.fillStyle=g;ctx.fillRect(0,0,W,H);';
  html += 'if(ma){var mg=ctx.createRadialGradient(mx,my,0,mx,my,MR);';
  html += 'mg.addColorStop(0,"rgba(255,217,61,0.1)");mg.addColorStop(1,"transparent");';
  html += 'ctx.fillStyle=mg;ctx.beginPath();ctx.arc(mx,my,MR,0,Math.PI*2);ctx.fill()}';
  html += 'var vc=ti?Math.floor(tidx):pts.length;';
  html += 'for(var i=0;i<vc;i++){var p=pts[i];if(!p)continue;';
  html += 'var sp=Math.sqrt((p.vx||0)*(p.vx||0)+(p.vy||0)*(p.vy||0));';
  html += 'var col=pal[i%pal.length];ctx.save();';
  html += 'ctx.shadowColor=col;ctx.shadowBlur=8+sp*4;';
  html += 'ctx.fillStyle=col;ctx.font="bold "+FS+"px sans-serif";';
  html += 'var tw=ctx.measureText(p.char).width;';
  html += 'ctx.fillText(p.char,p.x+(p.w-tw)/2,p.y+FS*0.85);ctx.restore()}';
  html += 'var n=performance.now();document.getElementById("fps").textContent=" fps:"+Math.round(1000/(n-lk+0.001));lk=n}';

  html += 'function lp(){upd();drw();requestAnimationFrame(lp)}lp();\n';

  // 控制函数
  html += 'function setW(m,btn){wm=m;';
  html += 'document.getElementById("b1").className=btn.id==="b1"?"btn on":"btn";';
  html += 'document.getElementById("b2").className=btn.id==="b2"?"btn on":"btn";';
  html += 'document.getElementById("wm").textContent=" \u6a21\u5f0f:"+m}';
  html += 'function tgG(btn){gr=!gr;btn.className=gr?"btn on":"btn"}';
  html += 'function exp(){pts.forEach(function(p){var a=Math.random()*Math.PI*2,';
  html += 'f=5+Math.random()*8;p.vx=Math.cos(a)*f;p.vy=Math.sin(a)*f})}';
  html += 'function rst(){pts=JSON.parse(JSON.stringify(INIT));tidx=0;ti=false;ma=false;';
  html += 'gr=false;document.getElementById("bg").className="btn";';
  html += 'document.getElementById("bt").className="btn";document.getElementById("ms").textContent=" \u7a7a\u95f2"}';
  html += 'function tgT(btn){ti=!ti;btn.className=ti?"btn on":"btn";if(ti)tidx=0}';

  html += '\n<\/script>\n';
  html += '</body>\n</html>';

  // 初始化显示
  html = html.replace('<span id="pc"></span>', '<span id="pc">\u7c92\u5b50\u6570\uff1a' + particles.length + '<br></span>');
  html = html.replace('<span id="fps"></span>', '<span id="fps">fps:--<br></span>');
  html = html.replace('<span id="wm"></span>', '<span id="wm">\u6a21\u5f0f:' + wrapMode + '<br></span>');
  html = html.replace('<span id="ms"></span>', '<span id="ms">\u9f20\u6807\uff1a\u7a7a\u95f2</span>');

  return html;
}

function main() {
  var args = process.argv.slice(2);
  var opts = {};
  for (var i = 0; i < args.length; i++) {
    var a = args[i];
    if (a === '--text') opts.text = args[++i];
    else if (a === '--font') opts.font = args[++i];
    else if (a === '--width') opts.canvasWidth = parseInt(args[++i]);
    else if (a === '--height') opts.canvasHeight = parseInt(args[++i]);
    else if (a === '--bg') opts.bgColor = args[++i];
    else if (a === '--color') opts.particleColor = args[++i];
    else if (a === '--wrap') opts.wrapMode = args[++i];
    else if (a === '--output') opts.output = args[++i];
    else if (a === '--help' || a === '-h') {
      console.log('Pretext 文字粒子自由运动引擎\n');
      console.log('用法: node scripts/particle-text.js --text "你好" [选项...]');
      console.log('  --text     粒子文字');
      console.log('  --font     字体（如 "32px sans-serif"）');
      console.log('  --width    Canvas 宽度');
      console.log('  --height   Canvas 高度');
      console.log('  --bg       背景色');
      console.log('  --color    粒子颜色');
      console.log('  --wrap     边界 bounce|wrap');
      console.log('  --output   html|info');
      console.log('\n示例: node scripts/particle-text.js --text "小星星绘本馆"');
      console.log('     node scripts/particle-text.js --text "Pretext" --output info');
      return;
    }
  }

  opts.text = opts.text || '你好，世界！Hello World!';
  opts.canvasWidth = opts.canvasWidth || 800;
  opts.canvasHeight = opts.canvasHeight || 500;
  opts.fontSize = parseFontSize(opts.font || '32px sans-serif');

  if (opts.output === 'info') {
    var lines = wrapLines(opts.text, opts.canvasWidth - 40, opts.fontSize);
    var totalChars = opts.text.length;
    console.log('\n Pretext 粒子分析');
    console.log('='.repeat(48));
    console.log('  文本: "' + opts.text + '"');
    console.log('  粒子数: ' + totalChars);
    console.log('  字号: ' + opts.fontSize + 'px');
    console.log('  Canvas: ' + opts.canvasWidth + ' x ' + opts.canvasHeight);
    console.log('  行数: ' + lines.length);
    console.log('-'.repeat(48));
    lines.forEach(function(l, i) {
      console.log('  第' + (i + 1) + '行: "' + l + '" (' + Math.round(estimateWidth(l, opts.fontSize)) + 'px)');
    });
    return;
  }

  var html = generateDemoHTML(opts);
  var outPath = path.join(SKILL_DIR, 'particle-text-demo.html');
  fs.writeFileSync(outPath, '\ufeff' + html, 'utf8');
  console.log('\n[OK] 粒子动画已生成：' + outPath);
  console.log('     粒子数：' + opts.text.length + ' 个字符\n');
}

if (require.main === module) main();
else module.exports = { generateDemoHTML: generateDemoHTML };
