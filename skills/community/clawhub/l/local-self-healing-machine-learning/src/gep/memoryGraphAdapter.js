// Memory Graph Adapter — local-only.
// Remote KG provider removed. All memory stays on disk.

const localGraph = require('./memoryGraph');

module.exports = {
  name: 'local',
  getAdvice(opts) { return localGraph.getMemoryAdvice(opts); },
  recordSignalSnapshot(opts) { return localGraph.recordSignalSnapshot(opts); },
  recordHypothesis(opts) { return localGraph.recordHypothesis(opts); },
  recordAttempt(opts) { return localGraph.recordAttempt(opts); },
  recordOutcome(opts) { return localGraph.recordOutcomeFromState(opts); },
  recordExternalCandidate(opts) { return localGraph.recordExternalCandidate(opts); },
  memoryGraphPath() { return localGraph.memoryGraphPath(); },
  computeSignalKey(signals) { return localGraph.computeSignalKey(signals); },
  tryReadMemoryGraphEvents(limit) { return localGraph.tryReadMemoryGraphEvents(limit); },
};
