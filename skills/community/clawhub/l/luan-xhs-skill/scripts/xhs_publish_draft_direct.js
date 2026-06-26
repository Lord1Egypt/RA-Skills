const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const disableProxy = require('./disable_proxy');

function sleep(ms){return new Promise(r=>setTimeout(r,ms));}

(async ()=>{
  const workspace = path.join(process.env.HOME,'.openclaw','workspace');
  const sessionPath = path.join(workspace,'xhs_user_info.json');
  const shot = path.join(workspace,'xhs_publish_draft_direct.png');
  if(!fs.existsSync(sessionPath)){ console.error('NO_SESSION'); process.exit(2); }
  const session = JSON.parse(fs.readFileSync(sessionPath,'utf8'));
  const browser = await chromium.launch({ headless:true, args:['--no-sandbox'] });
  const context = await browser.newContext({ viewport:{width:1400,height:960} });
  if(Array.isArray(session.cookies) && session.cookies.length) await context.addCookies(session.cookies).catch(()=>{});
  const page = await context.newPage();
  try{
    await page.goto('https://creator.xiaohongshu.com/new/note-manager',{waitUntil:'domcontentloaded', timeout:30000}).catch(()=>{});
    await page.waitForTimeout(2000);
    // click 草稿箱 tab if present
    try{ const draftTab = page.getByText('草稿箱', { exact: true }).first(); if(await draftTab.isVisible().catch(()=>false)){ await draftTab.click().catch(()=>{}); await page.waitForTimeout(1200); } }catch(e){}

    // find candidate draft nodes
    const candidates = await page.evaluate(() => {
      const nodes = Array.from(document.querySelectorAll('*'));
      const picks = [];
      for(const n of nodes){
        try{
          const txt = (n.innerText||'').trim().replace(/\s+/g,' ');
          if(!txt) continue;
          // heuristics: contains 草稿 or has 编辑 删除 controls
          if(txt.includes('草稿') || (txt.includes('编辑') && txt.includes('删除')) || txt.includes('暂存')){
            const h = n.querySelector('h3') || n.querySelector('h2') || n.querySelector('strong');
            const title = h ? (h.innerText || '').trim() : txt.split('\n')[0];
            const rect = n.getBoundingClientRect();
            if(rect && rect.width>20 && rect.height>10) picks.push({title: title.slice(0,200), x: Math.round(rect.x+rect.width/2), y: Math.round(rect.y+rect.height/2)});
          }
        }catch(e){}
      }
      return picks.slice(0,10);
    });

    if(!candidates || candidates.length===0){
      // fallback: find any '编辑' button and click nearest
      const editFound = await page.evaluate(() => {
        const nodes = Array.from(document.querySelectorAll('*'));
        const edit = nodes.find(n => (n.innerText||'').trim()==='编辑' || (n.innerText||'').trim().startsWith('编辑'));
        if(edit){ edit.click(); return true; } return false;
      }).catch(()=>false);
      if(!editFound){ await page.screenshot({path:shot}).catch(()=>{}); console.error('NO_DRAFT_FOUND'); await browser.close(); process.exit(3); }
      await page.waitForTimeout(1200);
    } else {
      // click first candidate by coordinate
      const c = candidates[0];
      await page.mouse.click(c.x, c.y).catch(()=>{});
      await page.waitForTimeout(1200);
    }

    // now we should be in editor or have an edit UI
    // attempt to find publish button directly
    // wait up to 30s for title input or publish button
    const start = Date.now(); let ready=false;
    while(Date.now()-start < 30000){
      const titleVisible = await page.locator('input[placeholder*="填写标题"]').first().isVisible().catch(()=>false);
      const publishVisible = await page.getByText('发布', { exact: true }).last().isVisible().catch(()=>false);
      if(titleVisible || publishVisible){ ready=true; break; }
      await page.waitForTimeout(1000);
    }
    if(!ready){ await page.screenshot({path:shot}).catch(()=>{}); console.error('DRAFT_EDITOR_NOT_READY'); await browser.close(); process.exit(4); }

    // click publish
    let clicked=false;
    try{
      const publishCandidates = [page.getByText('发布',{exact:true}).last(), page.locator('button:has-text("发布")').last(), page.locator('[role="button"]:has-text("发布")').last()];
      for(const loc of publishCandidates){ if(await loc.isVisible().catch(()=>false)){ try{ await loc.click({ timeout: 5000 }); clicked=true; break; }catch(e){} } }
    }catch(e){}
    if(!clicked){
      // fallback: try to find any element with '发布' via evaluate and click
      const ok = await page.evaluate(()=>{ const n=[...document.querySelectorAll('*')].find(x=> (x.innerText||'').includes('发布') && x.offsetParent!==null); if(n){ n.click(); return true; } return false; }).catch(()=>false);
      if(ok) clicked=true;
    }

    await page.waitForTimeout(8000);
    // verify published in manager
    await page.goto('https://creator.xiaohongshu.com/new/note-manager',{waitUntil:'domcontentloaded',timeout:30000}).catch(()=>{});
    await page.waitForTimeout(2000);
    const published = await page.evaluate(() => {
      const nodes = Array.from(document.querySelectorAll('*'));
      return nodes.some(n => (n.innerText||'').includes('已发布') || (n.innerText||'').includes('审核中'));
    }).catch(()=>false);

    await page.screenshot({path:shot}).catch(()=>{});
    if(published){ console.log(JSON.stringify({ok:true, screenshot:shot})); await browser.close(); process.exit(0); }
    else { console.error(JSON.stringify({ok:false,error:'PUBLISH_VERIFY_FAILED', screenshot:shot})); await browser.close(); process.exit(5); }

  }catch(e){ console.error('SCRIPT_EXCEPTION',String(e)); try{ await page.screenshot({path:shot}).catch(()=>{});}catch(e){} await browser.close(); process.exit(99);} 
})();