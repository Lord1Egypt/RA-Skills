chrome.runtime.onMessage.addListener((_msg, _sender, sendResponse) => {
  sendResponse({ result: null });
  return false;
});
