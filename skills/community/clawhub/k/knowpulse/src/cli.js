#!/usr/bin/env node
'use strict';
const fs=require('node:fs'), engine=require('./engine');
function main(args){
 if(args.length<2)throw Error('Usage: node src/cli.js <validate|ancestors|path|demo> <json-file> [topic-ids...]');
 const [cmd,file,...ids]=args,data=JSON.parse(fs.readFileSync(file,'utf8'));
 const graph=engine.buildGraph(data.topics,data.dependencies);
 if(cmd==='validate')return {ok:true,topicCount:graph.nodes.size,dependencyCount:data.dependencies.length,subjects:[...new Set(data.topics.map(t=>t.subject))]};
 if(cmd==='ancestors')return engine.ancestors(graph,ids[0]);
 if(cmd==='path')return engine.learningPath(graph,ids);
 if(cmd==='demo'){let s=engine.createSession(graph,ids.length?ids:['ai.agent']);s=engine.applyAnswer(graph,s,'ai.agent','wrong');s=engine.applyAnswer(graph,s,'ai.agent','wrong');return engine.summarize(graph,s)}
 throw Error('unknown command: '+cmd);
}
try{console.log(JSON.stringify(main(process.argv.slice(2)),null,2))}catch(e){console.error(e.message);process.exitCode=1}
