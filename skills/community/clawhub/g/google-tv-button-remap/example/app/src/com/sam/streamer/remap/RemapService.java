package com.sam.streamer.remap;

import android.accessibilityservice.AccessibilityService;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.KeyEvent;
import android.view.accessibility.AccessibilityEvent;

/**
 * RCU Remap - consume the remote's app-button key event before the launcher sees it.
 *
 *   Netflix button -> HID usage 0x0C0078 -> KEYCODE_BUTTON_4 (191)
 *
 * With FLAG_REQUEST_FILTER_KEY_EVENTS the accessibility key filter hands us real
 * hardware key events; returning true swallows the event so Google's own
 * GlobalKeyListener never fires and the stock app never launches. No root.
 *
 * Design rules for the shipped build:
 *   - NO input logging of any kind.
 *   - Behaviour gated by a user-visible preference ("enabled").
 *   - Everything that is not the target keycode passes straight through.
 */
public class RemapService extends AccessibilityService {

    public static final String PREFS = "remap";
    public static final String KEY_ENABLED = "enabled";
    public static final String KEY_TARGET = "target";

    private static final int BTN_NETFLIX = 191;              // KEYCODE_BUTTON_4
    private static final String DEFAULT_TARGET = "com.spotify.tv.android";

    private SharedPreferences prefs;

    private SharedPreferences prefs() {
        if (prefs == null) {
            prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        }
        return prefs;
    }

    @Override
    protected void onServiceConnected() {
        prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    @Override
    public boolean onKeyEvent(KeyEvent event) {
        if (!prefs().getBoolean(KEY_ENABLED, true)) {
            return false; // disabled: stock behaviour
        }
        if (event.getKeyCode() == BTN_NETFLIX) {
            if (event.getAction() == KeyEvent.ACTION_UP) {
                launchTarget();
            }
            return true; // consume DOWN + UP
        }
        return false;
    }

    private void launchTarget() {
        String pkg = prefs().getString(KEY_TARGET, DEFAULT_TARGET);
        Intent i = getPackageManager().getLaunchIntentForPackage(pkg);
        if (i == null) {
            return;
        }
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
        try {
            startActivity(i);
        } catch (Exception ignored) {
        }
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
    }

    @Override
    public void onInterrupt() {
    }
}
