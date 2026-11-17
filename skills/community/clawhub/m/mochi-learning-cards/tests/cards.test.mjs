import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs/promises';import path from 'node:path';import os from 'node:os';
import {prepare,validateCards,exportCards,paragraphs,tsv} from '../scripts/learning-cards.mjs';import {readLocal} from '../scripts/local-files.mjs';
const temp=()=>fs.mkdtemp(path.join(os.tmpdir(),'mochi-learning-cards-test-'));
const source='A draft is not a commitment. A review checks whether each action has an owner and a due date.\r\n\r\nA source quote is evidence of what the text says, not proof that its claim is true.\r\n';
const valid={question:'What should an action review check?',answer:'Its owner and due date.',sourceId:'P1',quote:'each action has an owner and a due date'};
test('prepare preserves exact source and bounded paragraphs, then exports supported text artifacts',async()=>{
 const workspace=await temp(),input=path.join(workspace,'source.md');await fs.writeFile(input,source);const e=await prepare({workspace,sourceFile:input,lang:'en',maxCards:2});assert.equal(e.sourceText,source);assert.equal(e.paragraphs.length,2);assert.match(e.sourceSha256,/^[a-f0-9]{64}$/);
 await fs.writeFile(e.cardsFile,JSON.stringify([valid]));const out=await exportCards({workspace,evidenceFile:e.evidenceFile});assert.equal(out.cards,1);const markdown=await fs.readFile(out.markdownFile,'utf8'),anki=await fs.readFile(out.tsvFile,'utf8');assert.match(markdown,/owner and due date/);assert.match(anki,/^#separator:Tab\n#html:false\n#columns:Front\tBack\n/);assert.match(await fs.readFile(out.reviewFile,'utf8'),/- \[ \] 1\./);await assert.rejects(exportCards({workspace,evidenceFile:e.evidenceFile}),/already exists/);assert.equal(await fs.readFile(input,'utf8'),source);
});
test('missing evidence, duplicate questions, unsafe card syntax and excessive counts fail before output',async()=>{
 const workspace=await temp(),input=path.join(workspace,'source.md');await fs.writeFile(input,source);const e=await prepare({workspace,sourceFile:input,maxCards:2});
 for(const cards of [[{...valid,quote:'a fabricated quote'}],[valid,{...valid,question:'  WHAT SHOULD AN ACTION REVIEW CHECK?  '}],[{...valid,answer:'<img src=x onerror=alert(1)>'}],[{...valid,answer:'[sound:unsafe.mp3]'}],[{...valid,other:'ignored?'}],[valid,valid,valid]])assert.throws(()=>validateCards(e,cards));
 const tampered={...e,paragraphs:[{id:'P1',text:'A fabricated source'}]};assert.throws(()=>validateCards(tampered,[valid]),/snapshot/);await fs.writeFile(e.cardsFile,JSON.stringify([{...valid,quote:'invented evidence'}]));await assert.rejects(exportCards({workspace,evidenceFile:e.evidenceFile}),/evidence quote/);await assert.rejects(fs.stat(path.join(workspace,'learning-cards')),/ENOENT/);
});
test('literal Markdown/code/pipe input is escaped and TSV formulas are inert text',async()=>{
 for(const value of ['=1+1','  +SUM(A1:A2)','\t-10','\u0000@cmd','\u200b=1','\ufeff  =1'])assert.ok(tsv(value).startsWith('"\''),value);assert.equal(tsv('ordinary "text"'),'"ordinary ""text"""');assert.equal(tsv('line\nbreak'),'"line break"');
 const workspace=await temp(),input=path.join(workspace,'source.md');await fs.writeFile(input,'`Fence` | evidence uses literal symbols.');const e=await prepare({workspace,sourceFile:input});await fs.writeFile(e.cardsFile,JSON.stringify([{question:' =1+1',answer:'  +1 | `code`',sourceId:'P1',quote:'`Fence` | evidence'}]));const out=await exportCards({workspace,evidenceFile:e.evidenceFile});const text=await fs.readFile(out.markdownFile,'utf8');assert.match(text,/\\`Fence\\` \\| evidence/);assert.match(await fs.readFile(out.tsvFile,'utf8'),/"'=1\+1"/);
});
test('bounded UTF8 inputs, outside paths and symlink/junction inputs are rejected',async()=>{
 assert.throws(()=>paragraphs(''));assert.throws(()=>paragraphs(Array(81).fill('A paragraph.').join('\n\n')));assert.equal(paragraphs('a'.repeat(2001)).length,2);
 const workspace=await temp(),outside=await temp(),input=path.join(workspace,'source.md');await fs.writeFile(input,'x'.repeat(65537));await assert.rejects(prepare({workspace,sourceFile:input}),/bounded/);await fs.writeFile(input,Buffer.from([0xff]));await assert.rejects(prepare({workspace,sourceFile:input}));await fs.writeFile(path.join(outside,'source.md'),'Outside source text.');await assert.rejects(prepare({workspace,sourceFile:path.join(outside,'source.md')}),/inside/);
 await fs.symlink(outside,path.join(workspace,'linked'),'junction');await assert.rejects(prepare({workspace,sourceFile:path.join(workspace,'linked','source.md')}),/Symlink/);
});
test('descriptor read never consumes an unbounded concurrent growth',async()=>{
 const workspace=await temp(),input=path.join(workspace,'source.txt');await fs.writeFile(input,'small');const original=fs.open;let injected=false;
 fs.open=async(...args)=>{const h=await original(...args);if(args[0]===input){const read=h.read.bind(h);h.read=async(...readArgs)=>{if(!injected){injected=true;await fs.appendFile(input,'x'.repeat(4000));}return read(...readArgs);};}return h;};
 try{await assert.rejects(readLocal(workspace,input,20),/grew or changed/);assert.equal(injected,true);}finally{fs.open=original;}
});
