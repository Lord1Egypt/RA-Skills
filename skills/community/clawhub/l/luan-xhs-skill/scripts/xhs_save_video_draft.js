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
  const args = parseArgs(process.argv);
  const video = String(args.video||'').trim();
  const title = normalizeTitle(args.title||'视频草稿');
  const body = normalizeBody(args.body||'');
  if(!video){ console.error('USAGE: node xhs_save_video_draft.js --video /path --title "..." --body "..."'); process.exit(2); }

  const workspace = path.join(process.env.HOME,'.openclaw','workspace');
  const sessionPath = path.join(workspace,'xhs_user_info.json');
  const shot = path.join(workspace,'xhs_save_draft_result.png');

  if(!fs.existsSync(sessionPath)){ console.error('NO_SESSION'); process.exit(3); }
  if(!fs.existsSync(video)){ console.error('VIDEO_NOT_FOUND:'+video); process.exit(4); }

  const configPath = path.join(__dirname,'..','_meta.json');
  let config = {useProxy:false};
  try{ config = JSON.parse(fs.readFileSync(configPath,'utf8')).config || config; }catch(e){}
  disableProxy.apply(config.useProxy!==true?false:true);

  const session = JSON.parse(fs.readFileSync(sessionPath,'utf8'));

  const browser = await chromium.launch({ headless: true, args:['--no-sandbox'] });
  const context = await browser.newContext({ viewport:{width:1440,height:960} });
  if(Array.isArray(session.cookies) && session.cookies.length) await context.addCookies(session.cookies).catch(()=>{});
  const page = await context.newPage();

  try{
    await page.goto('https://creator.xiaohongshu.com/publish/publish',{waitUntil:'domcontentloaded',timeout:60000}).catch(()=>{});
    await page.waitForTimeout(2000);

    // ensure upload video tab
    try{ const videoTab = page.getByText('上传视频',{exact:true}).last(); if(await videoTab.isVisible().catch(()=>false)){ await videoTab.click().catch(()=>{}); await page.waitForTimeout(1200);} }catch(e){}

    // upload
    let uploaded=false;
    try{ const fileInputs = await page.locator('input[type=file]').elementHandles(); for(const fi of fileInputs){ try{ await fi.setInputFiles(video); uploaded=true; break;}catch(e){} } }catch(e){}
    if(!uploaded){ try{ const fi = await page.$('input[type=file]'); if(fi){ await fi.setInputFiles(video); uploaded=true; } }catch(e){}
    }
    if(!uploaded){ await page.screenshot({path:shot}).catch(()=>{}); console.error('FILE_INPUT_NOT_FOUND'); await browser.close(); process.exit(5); }

    // wait for UI ready or processing status; up to 180s
    const start = Date.now(); const timeout = 180000; let ready=false;
    while(Date.now()-start < timeout){
      const editorVisible = await page.locator('.tiptap.ProseMirror').first().isVisible().catch(()=>false);
      const saveVisible = await page.getByText('保存','{exact:false}').first().isVisible().catch(()=>false).catch(()=>false);
      if(editorVisible || saveVisible) { ready=true; break; }
      await page.waitForTimeout(2000);
    }
    if(!ready){ await page.screenshot({path:shot}).catch(()=>{}); console.error('VIDEO_PROCESS_TIMEOUT'); await browser.close(); process.exit(6); }

    // fill title/body
    try{ const titleInput = page.locator('input[placeholder*="填写标题"]').first(); if(await titleInput.isVisible().catch(()=>false)){ await titleInput.fill(title).catch(()=>{}); await page.waitForTimeout(300);} }catch(e){}
    try{ const editor = page.locator('.tiptap.ProseMirror').first(); if(await editor.isVisible().catch(()=>false)){ await editor.click().catch(()=>{}); if(body) await page.keyboard.insertText(body).catch(()=>{}); await page.waitForTimeout(300);} }catch(e){}

    // try to click a draft/save button: prefer exact labels
    const labels = ['保存草稿','保存并离开','暂存离开','保存草稿并退出','保存','暂存'];
    let clicked=false;
    for(const lbl of labels){
      try{
        const el = page.getByText(lbl,{exact:true}).last();
        if(await el.isVisible().catch(()=>false)){
          await el.click().catch(()=>{});
          clicked=true; break;
        }
      }catch(e){}
    }
    // fallback: click any element that contains '保存' and is visible
    if(!clicked){
      try{
        const ok = await page.evaluate(()=>{
          const nodes=[...document.querySelectorAll('*')];
          const n = nodes.find(n=> (n.innerText||'').includes('保存') && n.offsetParent!==null);
          if(n){ n.click(); return true; } return false;
        }).catch(()=>false);
        if(ok) clicked=true;
      }catch(e){}
    }

    if(!clicked){ await page.screenshot({path:shot}).catch(()=>{}); console.error('SAVE_BUTTON_NOT_FOUND'); await browser.close(); process.exit(7); }

    await page.waitForTimeout(1500);
    // check 草稿箱
    await page.goto('https://creator.xiaohongshu.com/new/note-manager',{waitUntil:'domcontentloaded',timeout:30000}).catch(()=>{});
    await page.waitForTimeout(2000);
    // try to find in drafts area
    const isDraft = await page.evaluate((t)=>{
      const nodes = [...document.querySelectorAll('*')];
      return nodes.some(n=> (n.innerText||'').includes(t) && (n.innerText||'').includes('草稿')) || nodes.some(n=>(n.innerText||'').includes(t));
    }, title).catch(()=>false);
    await page.screenshot({path:shot}).catch(()=>{});
    if(isDraft){ console.log(JSON.stringify({ok:true, draft:true, title, screenshot:shot})); await browser.close(); process.exit(0); }
    else { console.error(JSON.stringify({ok:false,error:'SAVE_VERIFY_FAILED', screenshot:shot})); await browser.close(); process.exit(8); }

  }catch(e){ console.error('SCRIPT_EXCEPTION',String(e)); try{ await page.screenshot({path:shot}).catch(()=>{});}catch(e){} await browser.close(); process.exit(99); }
})();