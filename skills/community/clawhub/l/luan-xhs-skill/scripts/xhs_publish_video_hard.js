const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const disableProxy = require('./disable_proxy');
const { normalizeTitle, normalizeBody } = require('./normalize_copy');

function parseArgs(argv){
  const args = {};
  for(let i=2;i<argv.length;i++){
    const t=argv[i]; if(!t.startsWith('--')) continue; const k=t.slice(2); const next=argv[i+1]; if(!next||next.startsWith('--')) args[k]=true; else { args[k]=next; i++; }
  }
  return args;
}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}

(async()=>{
  const args=parseArgs(process.argv);
  const video=String(args.video||'').trim();
  const title=normalizeTitle(args.title||'视频');
  const body=normalizeBody(args.body||'');
  const visibility=String(args.visibility||'public').trim();
  if(!video){console.error('USAGE: node xhs_publish_video_hard.js --video /path --title "..." --body "..."'); process.exit(2);} 
  const workspace=path.join(process.env.HOME,'.openclaw','workspace');
  const sessionPath=path.join(workspace,'xhs_user_info.json');
  const shot=path.join(workspace,'xhs_video_publish_hard.png');
  if(!fs.existsSync(sessionPath)){console.error('NO_SESSION'); process.exit(3);} if(!fs.existsSync(video)){console.error('VIDEO_NOT_FOUND:'+video); process.exit(4);} 

  const config = JSON.parse(fs.readFileSync(path.join(__dirname,'..','_meta.json'),'utf8')).config||{};
  disableProxy.apply(config.useProxy!==true?false:true);

  const session = JSON.parse(fs.readFileSync(sessionPath,'utf8'));
  const browser = await chromium.launch({ headless:true, args:['--no-sandbox'] });
  const context = await browser.newContext({ viewport:{width:1440,height:980} });
  if(Array.isArray(session.cookies) && session.cookies.length) await context.addCookies(session.cookies).catch(()=>{});
  const page = await context.newPage();

  try{
    await page.goto('https://creator.xiaohongshu.com/publish/publish',{waitUntil:'domcontentloaded',timeout:60000}).catch(()=>{});
    await page.waitForTimeout(2000);
    // try to click 上传视频
    try{ const videoTab=page.getByText('上传视频',{exact:true}).last(); if(await videoTab.isVisible().catch(()=>false)){ await videoTab.click().catch(()=>{}); await page.waitForTimeout(1200);} }catch(e){}

    // upload video
    let uploaded=false;
    try{ const fileInputs=await page.locator('input[type=file]').elementHandles(); for(const fi of fileInputs){ try{ await fi.setInputFiles(video); uploaded=true; break; }catch(e){} } }catch(e){}
    if(!uploaded){ try{ const fi=await page.$('input[type=file]'); if(fi){ await fi.setInputFiles(video); uploaded=true; } }catch(e){}
    }
    if(!uploaded){ await page.screenshot({path:shot}).catch(()=>{}); console.error(JSON.stringify({ok:false,error:'FILE_INPUT_NOT_FOUND'})); await browser.close(); process.exit(5); }

    // aggressive wait & click loop (5 min)
    const start=Date.now(); const timeout=5*60*1000; let published=false; let step=0;
    while(Date.now()-start < timeout){
      step++;
      // try dismissing known overlays
      try{
        const dismissTexts=['我知道了','关闭','取消','稍后再说','忽略'];
        for(const t of dismissTexts){
          const el=page.getByText(t,{exact:true}).first(); if(await el.isVisible().catch(()=>false)){ await el.click().catch(()=>{}); await page.waitForTimeout(600); }
        }
      }catch(e){}

      // try click common publish-like buttons by scanning visible nodes
      try{
        const nodes = await page.$$('button,div[role="button"],a,span');
        for(const n of nodes){
          try{
            const txt = (await n.innerText()).trim(); if(!txt) continue;
            if(/发布|发布笔记|提交|完成|保存并离开|保存并退出|确定|立即发布|公开发布/.test(txt)){
              if(await n.isVisible().catch(()=>false)){
                await n.click().catch(()=>{});
                await page.waitForTimeout(1200);
              }
            }
          }catch(e){}
        }
      }catch(e){}

      // try clicking some coordinates near bottom-right area
      try{ await page.mouse.click(1200,920).catch(()=>{}); await page.waitForTimeout(1000);}catch(e){}

      // try evaluate click via DOM for any element contains '发布'
      try{
        const ok = await page.evaluate(()=>{
          const nodes=[...document.querySelectorAll('*')];
          const n = nodes.find(n=> (n.innerText||'').includes('发布') && n.offsetParent!==null);
          if(n){ n.click(); return true; } return false;
        }).catch(()=>false);
        if(ok) await page.waitForTimeout(1500);
      }catch(e){}

      // after clicks, check note manager
      try{ await page.goto('https://creator.xiaohongshu.com/new/note-manager',{waitUntil:'domcontentloaded',timeout:30000}).catch(()=>{}); await page.waitForTimeout(2000); const found=await page.evaluate((t)=>[...document.querySelectorAll('*')].some(el=> (el.innerText||'').includes(t)), title); if(found){ published=true; break; } }catch(e){}

      // navigate back to publish page to retry interactions
      try{ await page.goto('https://creator.xiaohongshu.com/publish/publish',{waitUntil:'domcontentloaded',timeout:30000}).catch(()=>{}); await page.waitForTimeout(1200);}catch(e){}

      await sleep(2000);
    }

    if(published){ await page.screenshot({path:shot}).catch(()=>{}); console.log(JSON.stringify({ok:true,title,screenshot:shot})); await browser.close(); process.exit(0); }
    else { await page.screenshot({path:shot}).catch(()=>{}); console.error(JSON.stringify({ok:false,error:'HARD_FAIL', screenshot:shot})); await browser.close(); process.exit(6); }

  }catch(e){ console.error('SCRIPT_EXCEPTION',String(e)); try{ await page.screenshot({path:shot}).catch(()=>{});}catch(e){} await browser.close(); process.exit(99); }
})();
