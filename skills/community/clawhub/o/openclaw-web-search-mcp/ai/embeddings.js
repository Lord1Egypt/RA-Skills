const natural = require("natural");

const tfidf = new natural.TfIdf();
const documents=[];

function embedText(text){

  tfidf.addDocument(text);
  documents.push(text);

  return {stored:true};
}

function semanticSearch(query){

  const results=[];

  documents.forEach((doc,i)=>{

    let score=0;

    tfidf.tfidfs(query,(j,val)=>{
      if(i===j) score=val;
    });

    results.push({doc,score});
  });

  results.sort((a,b)=>b.score-a.score);

  return results.slice(0,5);
}

module.exports={embedText,semanticSearch};