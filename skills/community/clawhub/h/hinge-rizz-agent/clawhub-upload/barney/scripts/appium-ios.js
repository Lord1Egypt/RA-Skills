#!/usr/bin/env node

const fs = require('fs');

const args = process.argv.slice(2);
const ELEMENT_KEY = 'element-6066-11e4-a52e-4f735466cecf';

function hasFlag(name) {
  return args.includes(name);
}

function getArg(name, fallback = '') {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  return args[index + 1] || fallback;
}

function serverUrl() {
  return getArg('--server', process.env.APPIUM_SERVER || 'http://127.0.0.1:4723');
}

function sessionId() {
  return getArg('--session-id', process.env.APPIUM_SESSION_ID || '');
}

async function request(method, pathname, body) {
  let response;
  try {
    response = await fetch(`${serverUrl()}${pathname}`, {
      method,
      headers: { 'content-type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    });
  } catch (error) {
    throw new Error(`Unable to reach Appium at ${serverUrl()}. Start Appium and try again.`);
  }

  const text = await response.text();
  const parsed = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(parsed.value?.message || `HTTP ${response.status}`);
  }
  return parsed;
}

function parseElementId(result) {
  const value = result?.value || {};
  return value[ELEMENT_KEY] || value.ELEMENT || '';
}

async function main() {
  if (hasFlag('--status')) {
    const result = await request('GET', '/status');
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--create-session')) {
    const capabilities = {
      platformName: 'iOS',
      'appium:automationName': getArg('--automation-name', process.env.APPIUM_AUTOMATION_NAME || 'XCUITest'),
      'appium:deviceName': getArg('--device-name', process.env.IOS_DEVICE_NAME || ''),
      'appium:platformVersion': getArg('--platform-version', process.env.IOS_PLATFORM_VERSION || ''),
      'appium:udid': getArg('--udid', process.env.IOS_UDID || ''),
      'appium:noReset': getArg('--no-reset', 'true') !== 'false',
      'appium:newCommandTimeout': Number(getArg('--new-command-timeout', process.env.APPIUM_NEW_COMMAND_TIMEOUT || '300'))
    };

    const bundleId = getArg('--bundle-id', process.env.IOS_BUNDLE_ID || '');
    if (bundleId) {
      capabilities['appium:bundleId'] = bundleId;
    }

    const wdaLocalPort = getArg('--wda-local-port', process.env.APPIUM_WDA_LOCAL_PORT || '');
    if (wdaLocalPort) {
      capabilities['appium:wdaLocalPort'] = Number(wdaLocalPort);
    }

    const mjpegServerPort = getArg('--mjpeg-server-port', process.env.APPIUM_MJPEG_SERVER_PORT || '');
    if (mjpegServerPort) {
      capabilities['appium:mjpegServerPort'] = Number(mjpegServerPort);
    }

    const xcodeOrgId = getArg('--xcode-org-id', process.env.APPIUM_XCODE_ORG_ID || '');
    if (xcodeOrgId) {
      capabilities['appium:xcodeOrgId'] = xcodeOrgId;
    }

    const xcodeSigningId = getArg('--xcode-signing-id', process.env.APPIUM_XCODE_SIGNING_ID || '');
    if (xcodeSigningId) {
      capabilities['appium:xcodeSigningId'] = xcodeSigningId;
    }

    const updatedWdaBundleId = getArg('--updated-wda-bundle-id', process.env.APPIUM_UPDATED_WDA_BUNDLE_ID || '');
    if (updatedWdaBundleId) {
      capabilities['appium:updatedWDABundleId'] = updatedWdaBundleId;
    }

    const showXcodeLog = getArg('--show-xcode-log', process.env.APPIUM_SHOW_XCODE_LOG || '');
    if (showXcodeLog) {
      capabilities['appium:showXcodeLog'] = showXcodeLog === 'true';
    }

    const useNewWda = getArg('--use-new-wda', process.env.APPIUM_USE_NEW_WDA || '');
    if (useNewWda) {
      capabilities['appium:useNewWDA'] = useNewWda === 'true';
    }

    const usePreinstalledWda = getArg('--use-preinstalled-wda', process.env.APPIUM_USE_PREINSTALLED_WDA || '');
    if (usePreinstalledWda) {
      capabilities['appium:usePreinstalledWDA'] = usePreinstalledWda === 'true';
    }

    const wdaLaunchTimeout = getArg('--wda-launch-timeout', process.env.APPIUM_WDA_LAUNCH_TIMEOUT || '');
    if (wdaLaunchTimeout) {
      capabilities['appium:wdaLaunchTimeout'] = Number(wdaLaunchTimeout);
    }

    const wdaStartupRetries = getArg('--wda-startup-retries', process.env.APPIUM_WDA_STARTUP_RETRIES || '');
    if (wdaStartupRetries) {
      capabilities['appium:wdaStartupRetries'] = Number(wdaStartupRetries);
    }

    const wdaStartupRetryInterval = getArg(
      '--wda-startup-retry-interval',
      process.env.APPIUM_WDA_STARTUP_RETRY_INTERVAL || ''
    );
    if (wdaStartupRetryInterval) {
      capabilities['appium:wdaStartupRetryInterval'] = Number(wdaStartupRetryInterval);
    }

    const derivedDataPath = getArg('--derived-data-path', process.env.APPIUM_DERIVED_DATA_PATH || '');
    if (derivedDataPath) {
      capabilities['appium:derivedDataPath'] = derivedDataPath;
    }

    const allowProvisioningDeviceRegistration = getArg(
      '--allow-provisioning-device-registration',
      process.env.APPIUM_ALLOW_PROVISIONING_DEVICE_REGISTRATION || ''
    );
    if (allowProvisioningDeviceRegistration) {
      capabilities['appium:allowProvisioningDeviceRegistration'] =
        allowProvisioningDeviceRegistration === 'true';
    }

    const result = await request('POST', '/session', {
      capabilities: {
        alwaysMatch: capabilities,
        firstMatch: [{}]
      }
    });

    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--delete-session')) {
    if (!sessionId()) throw new Error('Missing session id');
    const result = await request('DELETE', `/session/${sessionId()}`);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--source')) {
    if (!sessionId()) throw new Error('Missing session id');
    const result = await request('GET', `/session/${sessionId()}/source`);
    console.log(result.value || '');
    return;
  }

  if (hasFlag('--screenshot')) {
    if (!sessionId()) throw new Error('Missing session id');
    const result = await request('GET', `/session/${sessionId()}/screenshot`);
    const out = getArg('--out', 'ios-screenshot.png');
    fs.writeFileSync(out, Buffer.from(result.value, 'base64'));
    console.log(`Wrote ${out}`);
    return;
  }

  if (hasFlag('--find')) {
    if (!sessionId()) throw new Error('Missing session id');
    const using = getArg('--using', 'accessibility id');
    const value = getArg('--value');
    if (!value) throw new Error('Missing --value');
    const result = await request('POST', `/session/${sessionId()}/element`, { using, value });
    const id = parseElementId(result);
    console.log(id);
    return;
  }

  if (hasFlag('--activate-app')) {
    if (!sessionId()) throw new Error('Missing session id');
    const bundleId = getArg('--bundle-id', process.env.IOS_BUNDLE_ID || '');
    if (!bundleId) throw new Error('Missing --bundle-id');
    const result = await request('POST', `/session/${sessionId()}/appium/device/activate_app`, { bundleId });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--terminate-app')) {
    if (!sessionId()) throw new Error('Missing session id');
    const bundleId = getArg('--bundle-id', process.env.IOS_BUNDLE_ID || '');
    if (!bundleId) throw new Error('Missing --bundle-id');
    const result = await request('POST', `/session/${sessionId()}/appium/device/terminate_app`, { bundleId });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--tap')) {
    if (!sessionId()) throw new Error('Missing session id');
    const elementId = getArg('--element-id');
    if (!elementId) throw new Error('Missing --element-id');
    const result = await request('POST', `/session/${sessionId()}/element/${elementId}/click`, {});
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (hasFlag('--type')) {
    if (!sessionId()) throw new Error('Missing session id');
    const elementId = getArg('--element-id');
    const text = getArg('--text');
    if (!elementId || !text) throw new Error('Missing --element-id or --text');
    const result = await request('POST', `/session/${sessionId()}/element/${elementId}/value`, {
      text,
      value: Array.from(text)
    });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log('Usage:');
  console.log('  node appium-ios.js --status');
  console.log(
    '  node appium-ios.js --create-session --bundle-id com.example.app --device-name "iPhone" --wda-local-port 8101 --wda-launch-timeout 180000'
  );
  console.log('  node appium-ios.js --source --session-id <id>');
  console.log('  node appium-ios.js --find --session-id <id> --using "accessibility id" --value Inbox');
  console.log('  node appium-ios.js --activate-app --session-id <id> --bundle-id com.apple.Preferences');
  console.log('  node appium-ios.js --tap --session-id <id> --element-id <id>');
  console.log('  node appium-ios.js --type --session-id <id> --element-id <id> --text "hello there"');
  process.exit(1);
}

main().catch(error => {
  console.error(error.message);
  process.exit(1);
});
