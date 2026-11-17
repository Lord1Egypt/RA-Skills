module.exports = function resolveThreadId(cliThreadId, processEnv, fileEnv) {
  processEnv = processEnv || {};
  fileEnv = fileEnv || {};
  var enforce = String(processEnv.INFORMAT_AGENT_ENFORCE_THREAD_ID || "").toLowerCase() === "true";
  var serverThreadId = String(processEnv.INFORMAT_AGENT_THREAD_ID || "").trim();
  if (enforce) {
    if (!serverThreadId) {
      throw new Error("INFORMAT_AGENT_THREAD_ID is required for an isolated run");
    }
    return serverThreadId;
  }
  return String(cliThreadId || serverThreadId || fileEnv.INFORMAT_AGENT_THREAD_ID || "").trim();
};
