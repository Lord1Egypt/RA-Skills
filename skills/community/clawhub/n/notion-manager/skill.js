const NOTION_VERSION = "2025-09-03";
const BASE_URL = "https://api.notion.com/v1";

async function run(params = {}) {
  const op = params.input?.operation;
  const p = params.input?.params || {};
  const key = params.auth?.notionApiKey;

  if (!key) return {status:"error",error_type:"auth",message:"auth.notionApiKey required"};
  if (!op) return {status:"error",error_type:"validation",message:"input.operation required"};

  const headers = {"Authorization":`Bearer ${{key}}`,"Notion-Version":NOTION_VERSION,"Content-Type":"application/json"};

  try {
    let url, opts = {headers};
    switch(op) {
      case "search":
        url = `${BASE_URL}/search`;
        opts.method = "POST";
        opts.body = JSON.stringify({query:p.query||"",page_size:20});
        break;
      case "getPage":
        url = `${BASE_URL}/pages/${p.page_id}`;
        break;
      case "queryDataSource":
        url = `${BASE_URL}/data_sources/${p.data_source_id}/query`;
        opts.method = "POST";
        opts.body = JSON.stringify(p);
        break;
      case "createPage":
        url = `${BASE_URL}/pages`;
        opts.method = "POST";
        opts.body = JSON.stringify(p);
        break;
      case "updatePage":
        url = `${BASE_URL}/pages/${p.page_id}`;
        opts.method = "PATCH";
        opts.body = JSON.stringify({properties:p.properties});
        break;
      case "appendBlocks":
        url = `${BASE_URL}/blocks/${p.block_id}/children`;
        opts.method = "PATCH";
        opts.body = JSON.stringify({children:p.children});
        break;
      case "createDataSource":
        url = `${BASE_URL}/data_sources`;
        opts.method = "POST";
        opts.body = JSON.stringify(p);
        break;
      default:
        return {status:"error",error_type:"validation",message:`Unknown op: ${{op}}`};
    }

    const res = await fetch(url, opts);
    const data = await res.json();

    return res.ok 
      ? {status:"success",data,meta:{operation:op}}
      : {status:"error",error_type:"api",http_status:res.status,data};
  } catch(e) {
    return {status:"error",error_type:"network",message:e.message};
  }
}

module.exports = {run};
