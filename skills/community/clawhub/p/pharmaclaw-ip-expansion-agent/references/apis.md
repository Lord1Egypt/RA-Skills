# Patent/Compound APIs

## USPTO PatentsView (free JSON)
- Query: POST https://api.patentsview.org/patents/query
- Ex: {'q': {'_text_any': ['aspirin']}, 'f': ['patent_number']}
- Full: https://developer.uspto.gov/api-catalog

## PubChem PUG REST
- SMILES to CID: /pug/compound/smiles/{smiles}/cids/JSON
- Similarity: /pug/compound/fastsimilarity_2d/{name}/cids/JSON?Threshold=80

## EPO OPS (XML/JSON)
- https://developers.epo.org/ (key req'd for prod)

## ChEMBL
- pychembl: from chembl_webresource_client.new_client import new_client; c = new_client.Molecule

Rate limits: 5/sec USPTO.
