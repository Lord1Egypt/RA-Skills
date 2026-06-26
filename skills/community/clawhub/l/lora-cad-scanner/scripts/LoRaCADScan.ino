/*
 * LoRa CAD Scanner v4 — LilyGo T3 (SX1276 + SSD1306 128x64)
 * • Scans 433–445 MHz, 50 kHz step
 * • BW: 15.6 / 31.25 / 62.5 / 125 / 250 / 500 kHz | SF: 6–12
 * • CAD captures the first LoRa symbol (chirp)
 * • On CAD hit above threshold → 10-second RX window on the same frequency
 *   to capture a real packet (parsePacket)
 * • OLED: current parameters + RX window status + last packet
 * • 15-minute reports via Serial + Telegram through Pi
 *
 * Pins  LoRa: SCK=5 MISO=19 MOSI=27 SS=18 RST=23 DIO0=26
 *        OLED: SDA=21 SCL=22 addr=0x3C
 */

#include <SPI.h>
#include <Wire.h>
#include <LoRa.h>
#include <U8g2lib.h>

// ── Pins ─────────────────────────────────────────────────────────────────────
#define LORA_SCK   5
#define LORA_MISO  19
#define LORA_MOSI  27
#define LORA_SS    18
#define LORA_RST   23
#define LORA_DIO0  26
#define OLED_SDA   21
#define OLED_SCL   22

// ── SX1276 registers ─────────────────────────────────────────────────────────
#define REG_OP_MODE       0x01
#define REG_IRQ_FLAGS     0x12
#define REG_RSSI_WB       0x2C
#define REG_RSSI_PKT      0x1A    // packet RSSI after RX
#define REG_SNR_PKT       0x19    // packet SNR
#define REG_MODEM_CFG1    0x1D
#define REG_MODEM_CFG2    0x1E
#define REG_MODEM_CFG3    0x26
#define MODE_STDBY        0x81
#define MODE_RXCONT       0x85
#define MODE_CAD          0x87
#define IRQ_CAD_DONE      0x04
#define IRQ_CAD_DETECTED  0x01
#define IRQ_RX_DONE       0x40
#define IRQ_VALID_HDR     0x10

// ── Scan config ───────────────────────────────────────────────────────────────
#define FREQ_START          433000000UL
#define FREQ_END            445000000UL
#define FREQ_STEP             50000UL
#define CAD_TIMEOUT_MS        400
#define RX_WINDOW_MS        10000UL   // packet capture window after CAD hit
#define REPORT_INTERVAL_MS  (15UL * 60UL * 1000UL)

// ── Filters ───────────────────────────────────────────────────────────────────
#define RSSI_MIN_DBM   -130        // threshold to open RX window
#define CONFIRM_COUNT    2         // CAD hits before reporting

// ── BW table — includes 15.6 and 31.25 kHz ─────────────────────────────────
struct BwCfg { long hz; uint8_t code; const char* label; };
const BwCfg BWS[] = {
  {  15600, 3, " 15k" },   // BW 15.625 kHz — code 3
  {  31250, 4, " 31k" },   // BW 31.25 kHz  — code 4
  {  62500, 6, " 62k" },
  { 125000, 7, "125k" },
  { 250000, 8, "250k" },
  { 500000, 9, "500k" },
};
const int NUM_BW = 6;

// ── Hit log ───────────────────────────────────────────────────────────────────
#define MAX_HITS 80
struct HitEntry {
  unsigned long freq;
  int  bwHz, sf, rssiMin, rssiMax;
  uint16_t cadCount;   // CAD hits
  uint16_t pktCount;   // real packets captured
  bool isNew;
};
HitEntry hitLog[MAX_HITS];
int hitCount = 0;

// ── Last captured packet ───────────────────────────────────────────────────────
struct PktInfo {
  bool     valid;
  unsigned long freq;
  int      bwHz, sf, rssi, snr, len;
  uint8_t  payload[32];
  char     bwLabel[6];
};
PktInfo lastPkt = {false};

// ── OLED ──────────────────────────────────────────────────────────────────────
U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, OLED_SCL, OLED_SDA, U8X8_PIN_NONE);

// ── Register helpers ──────────────────────────────────────────────────────────
uint8_t readReg(uint8_t reg) {
  digitalWrite(LORA_SS, LOW);
  SPI.transfer(reg & 0x7F);
  uint8_t v = SPI.transfer(0);
  digitalWrite(LORA_SS, HIGH);
  return v;
}
void writeReg(uint8_t reg, uint8_t val) {
  digitalWrite(LORA_SS, LOW);
  SPI.transfer(reg | 0x80);
  SPI.transfer(val);
  digitalWrite(LORA_SS, HIGH);
}
void setBW(uint8_t code) {
  writeReg(REG_MODEM_CFG1, (readReg(REG_MODEM_CFG1) & 0x0F) | (code << 4));
}
void setSF(int sf) {
  // REG_MODEM_CFG2: SF[7:4]
  writeReg(REG_MODEM_CFG2, (readReg(REG_MODEM_CFG2) & 0x0F) | ((sf & 0x0F) << 4));
  // SF6 requires implicit header + detect optimize
  if (sf == 6) {
    writeReg(0x31, 0xc5);
    writeReg(0x37, 0x0c);
    writeReg(REG_MODEM_CFG1, readReg(REG_MODEM_CFG1) | 0x01); // implicit header
  } else {
    writeReg(0x31, 0xc3);
    writeReg(0x37, 0x0a);
    writeReg(REG_MODEM_CFG1, readReg(REG_MODEM_CFG1) & 0xFE); // explicit header
  }
  // LowDataRateOptimize for SF11/12 + BW<=62.5
  uint8_t cfg3 = readReg(REG_MODEM_CFG3) & 0xF7;
  if (sf >= 11) cfg3 |= 0x08;
  writeReg(REG_MODEM_CFG3, cfg3);
}

// ── CAD ───────────────────────────────────────────────────────────────────────
bool runCAD() {
  writeReg(REG_IRQ_FLAGS, 0xFF);
  writeReg(REG_OP_MODE, MODE_CAD);
  unsigned long t0 = millis();
  while (!(readReg(REG_IRQ_FLAGS) & IRQ_CAD_DONE)) {
    if (millis() - t0 > CAD_TIMEOUT_MS) {
      writeReg(REG_OP_MODE, MODE_STDBY);
      return false;
    }
  }
  bool hit = (readReg(REG_IRQ_FLAGS) & IRQ_CAD_DETECTED) != 0;
  writeReg(REG_IRQ_FLAGS, 0xFF);
  writeReg(REG_OP_MODE, MODE_STDBY);
  return hit;
}

// ── RX window — waiting for a real packet for 10 seconds ─────────────────────
bool tryReceivePacket(unsigned long freq, int bwHz, int sf,
                      const char* bwLabel, int cadRssi) {
  Serial.print(F("# RX_WINDOW "));
  Serial.print(freq); Serial.print(',');
  Serial.print(bwHz); Serial.print(',');
  Serial.println(sf);

  // Set up for RX with the same parameters
  LoRa.setFrequency(freq);
  LoRa.setSpreadingFactor(sf);
  setBW(BWS[0].code); // temporary, will be overwritten
  // Find the correct BW code
  for (int i = 0; i < NUM_BW; i++)
    if (BWS[i].hz == bwHz) { setBW(BWS[i].code); break; }
  setSF(sf);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();

  // OLED — waiting for packet mode
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_8x13B_tf);
  char buf[24];
  snprintf(buf, sizeof(buf), "%lu.%03lu", freq/1000000UL, (freq%1000000UL)/1000UL);
  u8g2.drawStr(0, 14, buf);
  u8g2.setFont(u8g2_font_5x7_tf);
  snprintf(buf, sizeof(buf), "BW:%s SF:%d  WAIT PKT", bwLabel, sf);
  u8g2.drawStr(0, 25, buf);
  u8g2.drawStr(0, 35, ">>> RX WINDOW 10s <<<");
  snprintf(buf, sizeof(buf), "CAD RSSI: %d dBm", cadRssi);
  u8g2.drawStr(0, 45, buf);
  u8g2.sendBuffer();

  // Switch to RX
  writeReg(REG_OP_MODE, MODE_RXCONT);

  unsigned long t0 = millis();
  bool gotPacket = false;

  while (millis() - t0 < RX_WINDOW_MS) {
    uint8_t irq = readReg(REG_IRQ_FLAGS);

    if (irq & IRQ_RX_DONE) {
      writeReg(REG_IRQ_FLAGS, 0xFF);

      // Read packet using library
      writeReg(REG_OP_MODE, MODE_STDBY);
      int pktSize = LoRa.parsePacket();
      if (pktSize > 0) {
        int pktRssi = LoRa.packetRssi();
        int pktSnr  = (int)(LoRa.packetSnr());
        int len = min(pktSize, (int)sizeof(lastPkt.payload));
        for (int i = 0; i < len; i++)
          lastPkt.payload[i] = LoRa.read();

        lastPkt.valid  = true;
        lastPkt.freq   = freq;
        lastPkt.bwHz   = bwHz;
        lastPkt.sf     = sf;
        lastPkt.rssi   = pktRssi;
        lastPkt.snr    = pktSnr;
        lastPkt.len    = len;
        strncpy(lastPkt.bwLabel, bwLabel, sizeof(lastPkt.bwLabel));

        // Report to Serial
        Serial.print(F("# PACKET "));
        Serial.print(freq); Serial.print(',');
        Serial.print(bwHz); Serial.print(',');
        Serial.print(sf);   Serial.print(',');
        Serial.print(pktRssi); Serial.print(',');
        Serial.print(pktSnr);  Serial.print(',');
        Serial.print(len);  Serial.print(',');
        // hex payload
        for (int i = 0; i < len; i++) {
          if (lastPkt.payload[i] < 16) Serial.print('0');
          Serial.print(lastPkt.payload[i], HEX);
        }
        Serial.println();

        gotPacket = true;

        // ── OLED Screen 2: PACKET! ─────────────────────────────────────────
        // Display until RX window expires, update every second
        unsigned long pktShowStart = millis();
        while (millis() - t0 < RX_WINDOW_MS) {
          u8g2.clearBuffer();

          // Title
          u8g2.setFont(u8g2_font_6x10_tf);
          u8g2.drawStr(0, 9, "\x10 PACKET CAUGHT! \x11");  // arrows

          // Frequency + parameters
          u8g2.setFont(u8g2_font_5x7_tf);
          snprintf(buf, sizeof(buf), "%lu.%03lu %s SF%d",
                   freq/1000000UL, (freq%1000000UL)/1000UL, bwLabel, sf);
          u8g2.drawStr(0, 19, buf);

          // RSSI / SNR / packet length
          snprintf(buf, sizeof(buf), "RSSI:%d SNR:%+d len:%d",
                   pktRssi, pktSnr, len);
          u8g2.drawStr(0, 28, buf);

          u8g2.drawHLine(0, 30, 128);

          // HEX dump — row 1: bytes 0-7
          char hex1[28] = "", hex2[28] = "";
          for (int i = 0; i < min(len, 8); i++) {
            char tmp[4];
            snprintf(tmp, sizeof(tmp), "%02X ", lastPkt.payload[i]);
            strncat(hex1, tmp, sizeof(hex1)-strlen(hex1)-1);
          }
          // HEX row 2: bytes 8-15
          for (int i = 8; i < min(len, 16); i++) {
            char tmp[4];
            snprintf(tmp, sizeof(tmp), "%02X ", lastPkt.payload[i]);
            strncat(hex2, tmp, sizeof(hex2)-strlen(hex2)-1);
          }
          u8g2.setFont(u8g2_font_5x7_tf);
          u8g2.drawStr(0, 40, hex1[0] ? hex1 : "--");
          u8g2.drawStr(0, 49, hex2[0] ? hex2 : "");

          // ASCII preview (bytes 0-15, non-printable → '.')
          char ascii[20] = "";
          for (int i = 0; i < min(len, 16); i++) {
            uint8_t c = lastPkt.payload[i];
            ascii[i] = (c >= 32 && c < 127) ? (char)c : '.';
          }
          ascii[min(len,16)] = 0;
          u8g2.drawStr(0, 58, ascii);

          // Window countdown
          int rem = (RX_WINDOW_MS - (millis()-t0)) / 1000;
          snprintf(buf, sizeof(buf), "%ds", rem);
          u8g2.drawStr(110, 58, buf);

          u8g2.sendBuffer();
          delay(1000);
        }

        // Continue listening for the remainder of the window (already exited main loop)
        writeReg(REG_OP_MODE, MODE_RXCONT);
      }
    }

    // Timer on OLED (refresh every 1 second)
    static unsigned long lastOledUpdate = 0;
    if (!gotPacket && millis() - lastOledUpdate > 1000) {
      lastOledUpdate = millis();
      int remaining = (RX_WINDOW_MS - (millis()-t0)) / 1000;
      static uint8_t animFrame = 0; animFrame++;

      u8g2.clearBuffer();

      // ── OLED Screen 1: RX ON ───────────────────────────────────────────
      // Title with animation
      u8g2.setFont(u8g2_font_6x10_tf);
      const char* anims[] = {"[  RX ON  ]","[ >RX ON< ]","[>>RX ON<<]","[ >RX ON< ]"};
      u8g2.drawStr(16, 9, anims[animFrame % 4]);

      // Frequency
      u8g2.setFont(u8g2_font_8x13B_tf);
      snprintf(buf, sizeof(buf), "%lu.%03lu",
               freq/1000000UL, (freq%1000000UL)/1000UL);
      u8g2.drawStr(0, 24, buf);

      // Parameters
      u8g2.setFont(u8g2_font_5x7_tf);
      snprintf(buf, sizeof(buf), "BW:%s  SF:%d  %ddBm", bwLabel, sf, cadRssi);
      u8g2.drawStr(0, 34, buf);

      // Progress bar (waiting)
      int elapsed = (int)(millis() - t0);
      int barW = (int)(elapsed * 128L / RX_WINDOW_MS);
      u8g2.drawFrame(0, 38, 128, 8);
      u8g2.drawBox(0, 38, barW, 8);

      // Countdown
      snprintf(buf, sizeof(buf), "Waiting pkt... %ds", remaining);
      u8g2.drawStr(0, 55, buf);

      // Blinking antenna
      if (animFrame % 2) {
        // Draw simple antenna icon
        u8g2.drawStr(110, 55, ")))");
      }

      u8g2.sendBuffer();
    }
    delayMicroseconds(500);
  }

  writeReg(REG_OP_MODE, MODE_STDBY);
  writeReg(REG_IRQ_FLAGS, 0xFF);

  if (!gotPacket) {
    Serial.println(F("# RX_WINDOW_TIMEOUT"));
  }
  return gotPacket;
}

// ── Hit tracking ──────────────────────────────────────────────────────────────
HitEntry* findHit(unsigned long freq, int bwHz, int sf) {
  for (int i = 0; i < hitCount; i++)
    if (hitLog[i].freq == freq && hitLog[i].bwHz == bwHz && hitLog[i].sf == sf)
      return &hitLog[i];
  return nullptr;
}
void recordHit(unsigned long freq, int bwHz, int sf, int rssi, bool isPkt) {
  HitEntry* e = findHit(freq, bwHz, sf);
  if (e) {
    if (!isPkt) e->cadCount++; else e->pktCount++;
    e->isNew = true;
    if (rssi < e->rssiMin) e->rssiMin = rssi;
    if (rssi > e->rssiMax) e->rssiMax = rssi;
    return;
  }
  if (hitCount < MAX_HITS) {
    HitEntry ne = { freq, bwHz, sf, rssi, rssi,
                    (uint16_t)(isPkt?0:1), (uint16_t)(isPkt?1:0), true };
    hitLog[hitCount++] = ne;
  }
}

// ── Serial report ─────────────────────────────────────────────────────────────
void printReport(uint32_t pass, uint32_t totalCad, uint32_t totalPkt) {
  int confirmed = 0;
  for (int i = 0; i < hitCount; i++)
    if (hitLog[i].cadCount >= CONFIRM_COUNT || hitLog[i].pktCount > 0) confirmed++;

  Serial.println(F("# REPORT_START"));
  Serial.print(F("# PASS=")); Serial.print(pass);
  Serial.print(F(" CAD_HITS=")); Serial.print(totalCad);
  Serial.print(F(" PACKETS=")); Serial.print(totalPkt);
  Serial.print(F(" CONFIRMED_CH=")); Serial.println(confirmed);

  for (int i = 0; i < hitCount; i++) {
    HitEntry& h = hitLog[i];
    if (h.cadCount < CONFIRM_COUNT && h.pktCount == 0) continue;
    Serial.print(h.isNew ? "NEW," : "OLD,");
    Serial.print(h.pktCount > 0 ? "PKT," : "CAD,");
    Serial.print(h.freq);    Serial.print(',');
    Serial.print(h.bwHz);   Serial.print(',');
    Serial.print(h.sf);     Serial.print(',');
    Serial.print(h.rssiMin); Serial.print(',');
    Serial.print(h.rssiMax); Serial.print(',');
    Serial.print(h.cadCount); Serial.print(',');
    Serial.println(h.pktCount);
    h.isNew = false;
  }
  Serial.println(F("# REPORT_END"));
}

// ── OLED draw (scan mode) ─────────────────────────────────────────────────────
void drawScanDisplay(unsigned long freq, const char* bwLabel, int sf, int rssi,
                     uint32_t pass, uint32_t cadHits, uint32_t pkts) {
  char buf[24];
  u8g2.clearBuffer();

  u8g2.setFont(u8g2_font_5x7_tf);
  u8g2.drawStr(0, 7, "LoRa CAD Scanner v4");
  u8g2.drawHLine(0, 9, 128);

  u8g2.setFont(u8g2_font_8x13B_tf);
  snprintf(buf, sizeof(buf), "%lu.%03lu MHz",
           freq/1000000UL, (freq%1000000UL)/1000UL);
  u8g2.drawStr(0, 24, buf);

  u8g2.setFont(u8g2_font_5x7_tf);
  snprintf(buf, sizeof(buf), "BW:%s  SF:%-2d  %ddBm", bwLabel, sf, rssi);
  u8g2.drawStr(0, 35, buf);

  snprintf(buf, sizeof(buf), "P:%-3lu CAD:%-4lu PKT:%-3lu",
           (unsigned long)pass, (unsigned long)cadHits, (unsigned long)pkts);
  u8g2.drawStr(0, 45, buf);

  u8g2.drawHLine(0, 47, 128);
  u8g2.setFont(u8g2_font_5x7_tf);
  if (lastPkt.valid) {
    snprintf(buf, sizeof(buf), "PKT %lu.%03lu SF%d %ddBm",
             lastPkt.freq/1000000UL, (lastPkt.freq%1000000UL)/1000UL,
             lastPkt.sf, lastPkt.rssi);
    u8g2.drawStr(0, 57, buf);
  } else {
    u8g2.drawStr(0, 57, "No packets yet");
  }

  int pct = (int)(((freq - FREQ_START) * 128UL) / (FREQ_END - FREQ_START));
  u8g2.drawBox(0, 62, pct, 2);
  u8g2.sendBuffer();
}

// ── Setup ─────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  delay(400);

  u8g2.begin();
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_6x10_tf);
  u8g2.drawStr(0, 14, "LoRa CAD v4");
  u8g2.drawStr(0, 28, "Init LoRa...");
  u8g2.sendBuffer();

  Serial.println(F("# LoRa CAD Scanner v4 (CAD+RX window)"));

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  if (!LoRa.begin(FREQ_START)) {
    u8g2.clearBuffer();
    u8g2.drawStr(0, 14, "LoRa FAILED");
    u8g2.drawStr(0, 28, "Check wiring!");
    u8g2.sendBuffer();
    Serial.println(F("# ERROR: LoRa init failed"));
    while (1) delay(1000);
  }

  uint8_t ver = readReg(0x42);
  Serial.print(F("# SX127x: 0x")); Serial.println(ver, HEX);
  Serial.println(F("# FREQ_HZ,BW_HZ,SF,RSSI,CAD_RAW,CAD_CONFIRMED"));

  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_6x10_tf);
  u8g2.drawStr(0, 14, "LoRa OK!");
  u8g2.drawStr(0, 28, "CAD+RX window mode");
  u8g2.drawStr(0, 42, "Starting...");
  u8g2.sendBuffer();
  delay(800);
}

// ── Main loop ─────────────────────────────────────────────────────────────────
void loop() {
  static uint32_t pass      = 0;
  static uint32_t totalCad  = 0;
  static uint32_t totalPkt  = 0;
  static unsigned long lastReport = 0;

  pass++;
  Serial.print(F("# PASS ")); Serial.println(pass);

  for (unsigned long freq = FREQ_START; freq <= FREQ_END; freq += FREQ_STEP) {
    for (int bwIdx = 0; bwIdx < NUM_BW; bwIdx++) {
      for (int sf = 6; sf <= 12; sf++) {

        // Setup
        writeReg(REG_OP_MODE, MODE_STDBY);
        delayMicroseconds(150);
        LoRa.setFrequency(freq);
        setBW(BWS[bwIdx].code);
        setSF(sf);
        LoRa.setCodingRate4(5);
        LoRa.disableCrc();  // CRC disabled for CAD — will be enabled on RX

        // RSSI
        writeReg(REG_OP_MODE, MODE_RXCONT);
        delayMicroseconds(800);
        int rssi = -157 + readReg(REG_RSSI_WB);
        writeReg(REG_OP_MODE, MODE_STDBY);
        delayMicroseconds(150);

        // CAD
        bool cadHit = runCAD();
        bool confirmed = cadHit && (rssi > RSSI_MIN_DBM);

        if (confirmed) {
          totalCad++;
          recordHit(freq, BWS[bwIdx].hz, sf, rssi, false);

          // Open RX window — attempt to capture real packet
          bool gotPkt = tryReceivePacket(freq, BWS[bwIdx].hz, sf,
                                         BWS[bwIdx].label, rssi);
          if (gotPkt) {
            totalPkt++;
            recordHit(freq, BWS[bwIdx].hz, sf, lastPkt.rssi, true);
          }
        }

        // OLED update
        if (sf == 6) {
          drawScanDisplay(freq, BWS[bwIdx].label, sf, rssi,
                          pass, totalCad, totalPkt);
        }

        // Serial log
        Serial.print(freq);           Serial.print(',');
        Serial.print(BWS[bwIdx].hz);  Serial.print(',');
        Serial.print(sf);             Serial.print(',');
        Serial.print(rssi);           Serial.print(',');
        Serial.print(cadHit ? 1 : 0); Serial.print(',');
        Serial.println(confirmed ? 1 : 0);
      }
    }
  }

  Serial.println(F("# SCAN_COMPLETE"));

  if (millis() - lastReport >= REPORT_INTERVAL_MS) {
    lastReport = millis();
    printReport(pass, totalCad, totalPkt);
  }
}
