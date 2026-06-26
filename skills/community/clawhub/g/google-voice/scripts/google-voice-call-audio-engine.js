#!/usr/bin/env node
const puppeteer = require('puppeteer-core');
const fs = require('fs');
async function makeCall(targetNumber, audioPath, duration, authuser='0') {
  const cookiePath = process.env.GV_COOKIE_PATH;
  if (!cookiePath) throw new Error('Set GV_COOKIE_PATH to a private cookie export outside the repo. Do not commit Google cookies.');
  if (!audioPath || !fs.existsSync(audioPath)) throw new Error('Audio file does not exist: ' + audioPath);
  const recordingPath = '/tmp/gv_recorded_incoming.webm';
  const executablePath = process.env.CHROMIUM_PATH || process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/chromium';
  const headless = process.env.GV_HEADLESS === '0' ? false : 'new';
  const browser = await puppeteer.launch({ executablePath, args: ['--no-sandbox','--disable-setuid-sandbox','--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream',`--use-file-for-fake-audio-capture=${audioPath}`,'--allow-file-access','--autoplay-policy=no-user-gesture-required'], headless });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf8'));
    await page.setCookie(...cookies);
    await page.goto(`https://voice.google.com/u/${authuser}/calls`, { waitUntil: 'networkidle2', timeout: 60000 });
    await new Promise(r => setTimeout(r, 5000));
    await page.evaluate(async (targetNumber) => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      const norm = s => (s || '').toLowerCase();
      const visible = el => !!(el && el.getClientRects && el.getClientRects().length);
      const click = el => { el.scrollIntoView({ block: 'center', inline: 'center' }); el.click(); };
      const buttons = () => Array.from(document.querySelectorAll('button,[role="button"]')).filter(visible);
      const findButton = patterns => buttons().find(b => patterns.some(p => norm(b.getAttribute('aria-label') || b.innerText || b.textContent).includes(p)));
      const findInput = () => Array.from(document.querySelectorAll('input,textarea,[contenteditable="true"]')).find(el => visible(el) && /(number|name|phone|search|号码|电话|名称)/i.test([el.placeholder, el.getAttribute('aria-label'), el.getAttribute('data-placeholder')].filter(Boolean).join(' '))) || Array.from(document.querySelectorAll('input,textarea,[contenteditable="true"]')).find(visible);
      const dial = findButton(['make a call','place a call','new call','call','拨打','呼叫']);
      if (dial) { click(dial); await sleep(1200); }
      let input = null; for (let i=0;i<20;i++){ input=findInput(); if(input) break; await sleep(500); }
      if (!input) throw new Error('Could not find number input');
      input.focus();
      if (input.isContentEditable) { input.textContent = targetNumber; input.dispatchEvent(new InputEvent('input',{bubbles:true,inputType:'insertText',data:targetNumber})); }
      else { input.value=''; input.dispatchEvent(new Event('input',{bubbles:true})); input.value=targetNumber; input.dispatchEvent(new Event('input',{bubbles:true})); }
      await sleep(800); input.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true})); await sleep(1500);
      let callBtn=null; for(let i=0;i<16;i++){ callBtn=findButton(['call','拨打','呼叫']); if(callBtn && !callBtn.disabled) break; await sleep(500); }
      if(!callBtn || callBtn.disabled) throw new Error('Could not find enabled call button');
      click(callBtn);
    }, targetNumber);
    await page.evaluate(async () => { window.chunks=[]; try { const stream=await navigator.mediaDevices.getUserMedia({audio:true}); const recorder=new MediaRecorder(stream); recorder.ondataavailable=e=>{ if(e.data.size>0) window.chunks.push(e.data); }; recorder.start(); window.myRecorder=recorder; } catch(err) { console.error('Recorder init failed: '+err.message); } });
    await new Promise(r => setTimeout(r, (parseInt(duration,10)||60)*1000));
    const audioBase64 = await page.evaluate(async () => { if(!window.myRecorder) return null; window.myRecorder.stop(); await new Promise(r=>setTimeout(r,2000)); const blob=new Blob(window.chunks,{type:'audio/webm'}); return new Promise(resolve=>{ const reader=new FileReader(); reader.onloadend=()=>resolve(reader.result.split(',')[1]); reader.readAsDataURL(blob); }); });
    if (audioBase64) fs.writeFileSync(recordingPath, Buffer.from(audioBase64, 'base64'));
    console.log(JSON.stringify({ ok:true, number:targetNumber, authuser, recordingPath: audioBase64 ? recordingPath : null }, null, 2));
  } finally { await browser.close(); }
}
makeCall(process.argv[2], process.argv[3], process.argv[4], process.argv[5]).catch(e => { console.error('google-voice-call-audio-engine:', e.message || e); process.exit(1); });
