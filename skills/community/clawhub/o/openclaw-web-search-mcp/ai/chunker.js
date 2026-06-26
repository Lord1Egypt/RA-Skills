function chunkText(text,size=1000){

  const chunks=[];

  for(let i=0;i<text.length;i+=size)
    chunks.push(text.slice(i,i+size));

  return chunks;
}

module.exports={chunkText};