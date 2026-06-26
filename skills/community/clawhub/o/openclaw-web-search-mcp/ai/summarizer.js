const natural = require("natural");

function summarizeText(text){

  const sentences = text.match(/[^\.!\?]+[\.!\?]+/g) || [];

  if (sentences.length === 0) {
    // If no sentences detected (e.g., no punctuation), return the text as is
    return text;
  }

  const tfidf = new natural.TfIdf();

  sentences.forEach(s=>tfidf.addDocument(s));

  const scores=[];

  sentences.forEach((s,i)=>{

    let score=0;

    tfidf.listTerms(i).forEach(t=>{
      score+=t.tfidf;
    });

    scores.push({sentence:s,score});
  });

  scores.sort((a,b)=>b.score-a.score);

  return scores.slice(0,3).map(s=>s.sentence).join(" ");
}

module.exports={summarizeText};