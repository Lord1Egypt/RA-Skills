# HCT Alarm Event Codes & Descriptions

This document lists the alarm event codes supported by HCT platform and their corresponding detailed descriptions for reference when subscribing.

## 1. Video Intercom
| Event Code  | Description                          |
|:------------|:-------------------------------------|
| `Msg140001` | Messages about video intercom events |

## 2. On-Board Monitoring
| Event Code  | Description                       |
|:------------|:----------------------------------|
| `Msg330001` | GPS Data Report                   |
| `Msg330101` | Alarm Triggered by Panic Button   |
| `Msg330102` | Alarm Input                       |
| `Msg330201` | Forward Collision Warning         |
| `Msg330202` | Headway Monitoring Warning        |
| `Msg330203` | Lane Deviation Warning            |
| `Msg330204` | Pedestrian Collision Warning      |
| `Msg330205` | Speed Limit Warning               |
| `Msg330301` | Blind Spot Warning                |
| `Msg330401` | Sharp Turn                        |
| `Msg330402` | Sudden Brake                      |
| `Msg330403` | Sudden Acceleration               |
| `Msg330404` | Rollover                          |
| `Msg330405` | Speeding                          |
| `Msg330406` | Collision                         |
| `Msg330407` | ACC ON                            |
| `Msg330408` | ACC OFF                           |
| `Msg330501` | Smoking                           |
| `Msg330502` | Using Mobile Phone                |
| `Msg330503` | Fatigue Driving                   |
| `Msg330504` | Distraction                       |
| `Msg330505` | Seatbelt Unbuckled                |
| `Msg330506` | Video Tampering                   |
| `Msg330507` | Yawning                           |
| `Msg330508` | Wearing IR Interrupted Sunglasses |
| `Msg330509` | Absence                           |
| `Msg330510` | Front Passenger Detection         |
| `Msg335000` | Person and Vehicle Match          |
| `Msg335001` | Person and Vehicle Mismatch       |

## 3. Authentication Event
| Event Code  | Description                                      |
|:------------|:-------------------------------------------------|
| `Msg110001` | Access Granted by Card and Fingerprint           |
| `Msg110002` | Access Granted by Card, Fingerprint, and PIN     |
| `Msg110003` | Access Granted by Card                           |
| `Msg110004` | Access Granted by Card and PIN                   |
| `Msg110005` | Access Granted by Fingerprint                    |
| `Msg110006` | Access Granted by Fingerprint and PIN            |
| `Msg110007` | Duress Alarm                                     |
| `Msg110008` | Access Granted by Face and Fingerprint           |
| `Msg110009` | Access Granted by Face and PIN                   |
| `Msg110010` | Access Granted by Face and Card                  |
| `Msg110011` | Access Granted by Face, PIN, and Fingerprint     |
| `Msg110012` | Access Granted by Face, Card, and Fingerprint    |
| `Msg110013` | Access Granted by Face                           |
| `Msg110018` | Access Granted via Combined Authentication Modes |
| `Msg110019` | Skin-Surface Temperature Measured                |
| `Msg110020` | Password Authenticated                           |
| `Msg110022` | Access Granted by Bluetooth                      |
| `Msg110023` | Access Granted via QR Code                       |
| `Msg110024` | Access Granted via Keyfob                        |
| `Msg110501` | Verifying Card Encryption Failed                 |
| `Msg110502` | Max. Card Access Failed Attempts                 |
| `Msg110505` | Card No. Expired                                 |
| `Msg110506` | Access Timed Out by Card and PIN                 |
| `Msg110507` | Access Denied - Door Remained Locked or Inactive |
| `Msg110509` | Access Denied by Card and PIN                    |
| `Msg110510` | Access Timed Out by Card, Fingerprint, and PIN   |
| `Msg110511` | Access Denied by Card, Fingerprint, and PIN      |
| `Msg110512` | Access Denied by Card and Fingerprint            |
| `Msg110513` | Access Timed Out by Card and Fingerprint         |
| `Msg110514` | No Access Level Assigned                         |
| `Msg110515` | Card No. Does Not Exist                          |
| `Msg110516` | Invalid Time Period                              |
| `Msg110517` | Fingerprint Does Not Exist                       |
| `Msg110518` | Access Denied by Fingerprint                     |
| `Msg110519` | Access Denied by Fingerprint and PIN             |
| `Msg110520` | Access Timed Out by Fingerprint and PIN          |
| `Msg110521` | Access Denied by Face and Fingerprint            |
| `Msg110522` | Access Timed Out by Face and Fingerprint         |
| `Msg110523` | Access Denied by Face and PIN                    |
| `Msg110524` | Access Timed Out by Face and PIN                 |
| `Msg110525` | Access Denied by Face and Card                   |
| `Msg110526` | Access Timed Out by Face and Card                |
| `Msg110527` | Access Denied by Face, PIN, and Fingerprint      |
| `Msg110528` | Access Timed Out by Face, PIN, and Fingerprint   |
| `Msg110529` | Access Denied by Face, Card, and Fingerprint     |
| `Msg110530` | Access Timed Out by Face, Card, and Fingerprint  |
| `Msg110531` | Access Denied by Face                            |
| `Msg110533` | Live Facial Detection Failed                     |
| `Msg110545` | Combined Authentication Timed Out                |
| `Msg110546` | Access Denied by Invalid M1 Card                 |
| `Msg110547` | Verifying CPU Card Encryption Failed             |
| `Msg110548` | Access Denied - NFC Card Reading Disabled        |
| `Msg110549` | EM Card Reading Not Enabled                      |
| `Msg110550` | M1 Card Reading Not Enabled                      |
| `Msg110551` | CPU Card Reading Disabled                        |
| `Msg110552` | Authentication Mode Mismatch                     |
| `Msg110554` | Max. Card and Password Authentication Times      |
| `Msg110555` | Password Mismatches                              |
| `Msg110556` | Employee ID Does Not Exist                       |
| `Msg110557` | Access Denied: Scheduled Sleep Mode              |
| `Msg110559` | Verifying Desfire Card Encryption Failed         |
| `Msg110560` | Absence                                          |
| `Msg110561` | Authentication Failed Due to Abnormal Features   |
| `Msg110564` | Access Denied by Bluetooth                       |
| `Msg110565` | Access Denied by QR Code                         |
| `Msg110566` | Verifying QR Code Secret Key Failed              |
| `Msg110567` | Access Denied via Keyfob                         |
