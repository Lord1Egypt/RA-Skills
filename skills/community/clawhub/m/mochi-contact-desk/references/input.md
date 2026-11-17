# JSON actions

Actions put(contact), search(query), duplicates, import(file,apply default false), merge(target,sources:[ids],choose:{name,organization,notes} optional), followup(id optional,contactId,note,date,nextDate optional), due(date), export(format csv|vcard,output optional). Contact {id optional,name,emails:[strings],phones:[strings],tags:[strings],organization,notes}. Import <=5MiB /2000 contacts. Stable content-based IDs deduplicate identical repeated imports. Exports refuse an existing output file. Data in .mochilab/contact-desk, no external service or paid API.
