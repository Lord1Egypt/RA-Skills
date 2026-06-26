using System;
using System.IO;
using System.Text;
using System.Collections.Generic;

class Program
{
    static readonly string[] FramesToClear = new string[]
    {
        "TIT2", "TALB", "TPE1", "TPE2", "TPE3", "TOPE", "TCOM",
        "TCON", "TYER", "TDAT", "TRCK", "TPOS", "TENC", "TEXT",
        "COMM", "APIC", "TXXX", "WOAR", "WOAF", "WORS", "WPAY",
        "WPUB", "MCDI", "ETCO", "MLLT", "SYTC", "RVAD", "EQUA",
        "IPLS", "LINK", "POSS", "USER", "OWNE", "COMR", "ENCR",
        "GRID", "PRIV", "USLT", "SYLT", "GEOB", "RF64"
    };

    static void Main(string[] args)
    {
        string fileListPath = @"C:\Users\Haiyang\AppData\Local\Temp\mp3files_1_100_utf8.txt";
        string tempDir = @"C:\Temp\MP3Work_ID3";

        try
        {
            if (Directory.Exists(tempDir))
                Directory.Delete(tempDir, true);
            Directory.CreateDirectory(tempDir);

            string[] files = File.ReadAllLines(fileListPath, Encoding.UTF8);
            int success = 0;
            int failed = 0;

            foreach (string origPath in files)
            {
                if (string.IsNullOrWhiteSpace(origPath) || !File.Exists(origPath))
                    continue;

                string fileName = Path.GetFileName(origPath);
                string tempPath = Path.Combine(tempDir, fileName);

                try
                {
                    File.Copy(origPath, tempPath, true);

                    if (ClearAllID3(tempPath))
                    {
                        File.Copy(tempPath, origPath, true);
                        success++;
                        Console.WriteLine("OK: " + fileName);
                    }
                    else
                    {
                        failed++;
                        Console.WriteLine("FAIL: " + fileName);
                    }
                }
                catch (Exception ex)
                {
                    failed++;
                    Console.WriteLine("ERROR: " + fileName + " - " + ex.Message);
                }
                finally
                {
                    if (File.Exists(tempPath))
                        File.Delete(tempPath);
                }
            }

            Console.WriteLine("\nDone. Success: " + success + ", Failed: " + failed);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Fatal error: " + ex.Message);
        }
        finally
        {
            if (Directory.Exists(tempDir))
                Directory.Delete(tempDir, true);
        }
    }

    static bool ClearAllID3(string filePath)
    {
        byte[] allData = File.ReadAllBytes(filePath);
        long fileLen = allData.Length;

        // Parse ID3v1 at end (128 bytes, starts with "TAG")
        int id3v1Len = 0;
        if (fileLen >= 128)
        {
            if (allData[fileLen - 128] == 'T' && allData[fileLen - 127] == 'A' && allData[fileLen - 126] == 'G')
                id3v1Len = 128;
        }

        // Parse ID3v2 at start (starts with "ID3")
        int id3v2Len = 0;
        if (fileLen >= 10)
        {
            if (allData[0] == 'I' && allData[1] == 'D' && allData[2] == '3')
            {
                int sb1 = allData[6];
                int sb2 = allData[7];
                int sb3 = allData[8];
                int sb4 = allData[9];
                id3v2Len = 10 + (((sb1 & 0x7F) << 21) | ((sb2 & 0x7F) << 14) | ((sb3 & 0x7F) << 7) | (sb4 & 0x7F));
            }
        }

        // Extract MP3 data (between ID3v2 and ID3v1)
        long mp3Start = id3v2Len;
        long mp3End = fileLen - id3v1Len;
        long mp3Len = mp3End - mp3Start;
        if (mp3Len < 0) mp3Len = 0;

        // Process ID3v2 frames - filter out unwanted frames
        List<byte> newV2Frames = new List<byte>();
        int v2DataLen = id3v2Len - 10; // exclude 10-byte header
        int pos = 10; // start after ID3v2 header

        while (pos <= (id3v2Len - 10))
        {
            if (pos + 10 > allData.Length)
                break;

            string frameId = Encoding.ASCII.GetString(allData, pos, 4);
            int frameSize =
                (allData[pos + 4] << 24) |
                (allData[pos + 5] << 16) |
                (allData[pos + 6] << 8) |
                allData[pos + 7];

            // Frame must be at least 10 bytes (header)
            if (frameSize <= 0 || pos + 10 + frameSize > id3v2Len)
                break;

            bool clear = false;
            for (int i = 0; i < FramesToClear.Length; i++)
            {
                if (frameId == FramesToClear[i])
                {
                    clear = true;
                    break;
                }
            }

            if (!clear)
            {
                for (int i = 0; i < 10; i++)
                    newV2Frames.Add(allData[pos + i]);
                for (int i = 0; i < frameSize; i++)
                    newV2Frames.Add(allData[pos + 10 + i]);
            }

            pos += 10 + frameSize;
        }

        // Build new file: ID3v2 header + filtered frames + MP3 data (NO ID3v1)
        long newLen = 10 + newV2Frames.Count + mp3Len;
        byte[] newData = new byte[newLen];

        int writePos = 0;

        // ID3v2 header
        if (newV2Frames.Count > 0)
        {
            newData[writePos++] = (byte)'I';
            newData[writePos++] = (byte)'D';
            newData[writePos++] = (byte)'3';
            newData[writePos++] = 3; // version 2.3
            newData[writePos++] = 0;
            newData[writePos++] = 0;
            int sz = newV2Frames.Count;
            newData[writePos++] = (byte)((sz >> 21) & 0x7F);
            newData[writePos++] = (byte)((sz >> 14) & 0x7F);
            newData[writePos++] = (byte)((sz >> 7) & 0x7F);
            newData[writePos++] = (byte)(sz & 0x7F);

            for (int i = 0; i < newV2Frames.Count; i++)
                newData[writePos++] = newV2Frames[i];
        }

        // MP3 data
        if (mp3Len > 0)
        {
            Array.Copy(allData, mp3Start, newData, writePos, mp3Len);
        }

        File.WriteAllBytes(filePath, newData);
        return true;
    }
}
