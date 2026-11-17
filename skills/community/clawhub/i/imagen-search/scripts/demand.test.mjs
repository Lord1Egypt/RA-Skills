import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp,writeFile,rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { previewDemand,submitDemand } from './demand.mjs';
async function fixture(t) { const dir=await mkdtemp(path.join(tmpdir(),'imagen-demand-'));t.after(()=>rm(dir,{recursive:true,force:true}));return path.join(dir,'request.json'); }
const payload={email:'creator@example.test',request:'Roman aqueduct builders, landscape illustration',locale:'en'};
test('preview is local; missing consent and changed payload cannot submit',async t=>{
 const file=await fixture(t);await writeFile(file,JSON.stringify(payload));let calls=0;
 const client={request:async()=>{calls++;return {public_id:'receipt',status:'new'};}};
 const preview=await previewDemand(file);assert.equal(calls,0);assert.deepEqual(preview.payload,payload);
 await assert.rejects(()=>submitDemand(client,file),/consent/);assert.equal(calls,0);
 await writeFile(file,JSON.stringify({...payload,request:'A different request'}));
 await assert.rejects(()=>submitDemand(client,file,preview.confirmation),/changed/);assert.equal(calls,0);
});
test('only approved allowlisted fields are sent and the receipt is returned',async t=>{
 const file=await fixture(t);await writeFile(file,JSON.stringify(payload));const preview=await previewDemand(file);
 const result=await submitDemand({request:async(route,options)=>{assert.equal(route,'/gallery/demand-requests');assert.deepEqual(options,{method:'POST',body:payload});return {public_id:'receipt',status:'new'};}},file,preview.confirmation);
 assert.deepEqual(result.submitted,payload);assert.equal(result.receipt.public_id,'receipt');
});
test('extra context is rejected before any submission',async t=>{
 const file=await fixture(t);await writeFile(file,JSON.stringify({...payload,article:'private draft'}));
 await assert.rejects(()=>previewDemand(file),/Remove all other context/);
});
