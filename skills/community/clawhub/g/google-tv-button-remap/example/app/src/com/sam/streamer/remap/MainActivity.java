package com.sam.streamer.remap;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.provider.Settings;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Switch;
import android.widget.TextView;

/**
 * Minimal keeper UI (D-pad navigable, no touch needed on Android TV):
 *   - shows whether the accessibility service is enabled
 *   - an on/off switch for the remap
 *   - a shortcut to the system Accessibility settings
 */
public class MainActivity extends Activity {

    private SharedPreferences prefs;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        prefs = getSharedPreferences(RemapService.PREFS, Context.MODE_PRIVATE);

        float d = getResources().getDisplayMetrics().density;
        int pad = (int) (24 * d);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(pad, pad, pad, pad);

        TextView title = new TextView(this);
        title.setText("Remote App-Button Remap");
        title.setTextSize(24f);
        root.addView(title);

        TextView status = new TextView(this);
        status.setTextSize(16f);
        root.addView(status);

        TextView hint = new TextView(this);
        hint.setTextSize(14f);
        hint.setText("Android TV has no touch: use the D-pad, press OK to toggle.");
        root.addView(hint);

        Switch sw = new Switch(this);
        sw.setText("Netflix button -> Spotify");
        sw.setChecked(prefs.getBoolean(RemapService.KEY_ENABLED, true));
        sw.setOnCheckedChangeListener((v, checked) ->
                prefs.edit().putBoolean(RemapService.KEY_ENABLED, checked).apply());
        root.addView(sw);

        Button open = new Button(this);
        open.setText("Open Accessibility Settings");
        open.setOnClickListener(v ->
                startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)));
        root.addView(open);

        setContentView(root, new ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        updateStatus(status);
    }

    private void updateStatus(TextView status) {
        boolean enabled = prefs.getBoolean(RemapService.KEY_ENABLED, true);
        status.setText("Remap: " + (enabled ? "ON" : "OFF")
                + "  |  need the accessibility service enabled for it to act.");
    }
}
