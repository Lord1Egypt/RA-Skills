# Publishing

## Publishing Web
## PlayCanvas Hosting
Fastest, easiest way. One-click publish to playcanvas.com.
**Publish a Build:**
1. Click Publish button (left toolbar) or Menu → Publishing
2. Click **PUBLISH** next to "Publish on PlayCanvas"
3. Configure: Image, Title, Description, Version, Release Notes
4. Options: Concatenate Scripts, Minify Scripts, Generate Source Map, Optimize Scene Format
5. Select scenes (first-scene-banner = initial load) → **PUBLISH NOW**
**Primary Build:** What users see on the project PLAY button.
- Build URL: `https://playcanv.as/b/BUILD_ID/` (permanent until deleted)
- Primary link: `https://playcanv.as/p/PROJECT_ID/` (always latest)
- First publish auto-sets Primary; promote later builds manually
### iframe Embedding
```html
```
### Download ZIP
1. Editor → Publish → **DOWNLOAD .ZIP**
2. Name export, select scenes, click DOWNLOAD
3. Extract and serve — **cannot** open index.html via file://
**Local server options:**
- `python -m SimpleHTTPServer` → `http://localhost:8000`
- `npx http-server -p 8000 --cors -c-1`
- XAMPP / Apache / nginx
### GitHub Pages
Add `.nojekyll` file to repo root (prevents ignoring underscore-prefixed files). Deploy as standard static site.
## Publishing Mobile
PlayCanvas games are web pages. To submit to app stores, convert to native apps.
## Apache Cordova (Open Source)
Wraps web technologies in native containers for iOS, Android, macOS, Windows.
```bash
cordova create mygame com.example.mygame "My Game"
```
**Adding your app:** Delete `www/` contents, copy PlayCanvas files in. ⚠️ Audio must be Base64 for iOS WebView. Use the [official tool](https://github.com/playcanvas/playcanvas-rest-api-tools#cordova-publish) for Editor projects.
**iOS build (macOS only):**
```bash
cordova platform add ios  # v6.0.0+ (WKWebView)
```
Add to `config.xml` for cross-origin fixes:
```xml
<platform name="ios">
  <preference name="scheme" value="app" />
  <preference name="hostname" value="localhost" />
</platform>
```
Test: `cordova run ios` (Simulator) or Xcode → physical device → App Store Connect.
## GoNative (Paid)
[GoNative](https://gonative.io/) creates native apps from a URL via WebView. Requires online connectivity. Integrates native plugins: AdMob, In-App Purchases. [Plugin list](https://gonative.io/plugins).
## WebView
Build a native app with a fullscreen WebView loading your PlayCanvas app from local resources.
## Publishing Playable Ads
## Facebook Playable Ads
Use the [official tool](https://github.com/playcanvas/playcanvas-rest-api-tools).
**Size budget:** Engine ~1.2MB, Base64 adds ~30%. Single HTML: ~500KB for assets; ZIP: ~3MB. Minimize images (TinyPNG).
**Single HTML (2MB limit):**
```json
"one_page": { "patch_xhr_out": true, "inline_game_scripts": true, "extern_files": false }
```
**ZIP (5MB limit):**
```json
"one_page": { "patch_xhr_out": true, "inline_game_scripts": true, "extern_files": true }
```
Call `FbPlayableAd.onCTAClick()` in your CTA callback. Run: `npm run one-page`. Test in Facebook ad manager.
## Snapchat Playable Ads
Uses MRAID 2.0 standard. Soft limit: 5MB, ~3MB for assets.
Must call `snapchatCta()` as CTA callback. Requires unique folder name + external assets.
**Config:**
```json
"one_page": {
  "patch_xhr_out": false, "inline_game_scripts": true,
  "extern_files": { "enabled": true, "folder_name": "<GUID>", "external_url_prefix": "" },
  "mraid_support": true, "snapchat_cta": true
}
```
**Test:** Android [Creative Preview](https://play.google.com/store/apps/details?id=com.google.android.apps.audition) app + [ngrok](https://ngrok.com/) HTTPS tunnel.
**Final:** Set `external_url_prefix` to `https://rtb-ads.shadow.snapads.com/html5` for delivery.
