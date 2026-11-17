from helpers import *
from collections import Counter

PHRASES=['in conclusion','it is important to note','delve into','unlock the potential','总而言之','值得注意的是','在当今时代','赋能']
def facts(t):return Counter(re.findall(r'https?://[^\s<>]+|\d+(?:[.,]\d+)*(?:%|元|美元|USD)?',t))
def handle(s,r):
 action=r.get('action')
 if action=='lint':
  t=textfile(s.root,r['file']);issues=[]
  for n,line in enumerate(t.splitlines(),1):
   for phrase in PHRASES:
    if phrase.casefold() in line.casefold():issues.append({'line':n,'rule':'generic-phrase','phrase':phrase})
   for sent in re.split(r'(?<=[。！？.!?])\s*',line):
    if len(sent)>160 or len(sent.split())>35:issues.append({'line':n,'rule':'long-sentence','characters':len(sent)})
  paragraphs=[x.strip() for x in re.split(r'\n\s*\n',t) if x.strip()];repeats=[{'paragraph':k[:160],'count':v} for k,v in Counter(paragraphs).items() if v>1]
  return s.report({'findings':issues,'repeatedParagraphs':repeats,'factTokens':dict(facts(t)),'disclaimer':'Style hints, not an AI-authorship detector. Preserve facts and the author voice.'})
 if action=='compare':
  a=facts(textfile(s.root,r['before']));b=facts(textfile(s.root,r['after']));return s.report({'removedOrReduced':dict(a-b),'addedOrIncreased':dict(b-a),'factTokensUnchanged':a==b,'semanticAccuracyVerified':False})
 raise ValueError('Actions: lint, compare')
