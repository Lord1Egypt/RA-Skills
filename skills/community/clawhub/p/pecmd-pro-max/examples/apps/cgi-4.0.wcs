SET  ::WM_LBUTTONDOWN=0x0201
SET  ::WM_LBUTTONDBLCLK=0x0203
SET  ::WM_MOUSEHOVER=0x02A1
SET  ::WM_MOUSELEAVE=0x02A3
TEAM ENVI &&vFORM=|ENVI &&LnvFORM=|ENVI &&PARTSEL1=|ENVI &&PARTSEL2=|ENVI &&PARTSEL5=|ENVI &&CheckGHOSize=0
TEAM ENVI &&P2PList=|ENVI &&FFDrv=|ENVI$ &&NLDD=0d 0a|ENVI$ &&NLHH=0a|ENVI$ &&TAB=09|ENVI &&GinCD=|ENVI &&ahCHECK=|ENVI &&PEPOS=0
TEAM ENVI &&HDMHINFO=|ENVI &&HDSEL=|ENVI &&HDLIST=|ENVI &&IsWOW64=WOW32|ENVI &&PLIST1ITEM=|ENVI &&DLIST1ITEM=|ENVI &&ILIST1ITEM=
TEAM ENVI &&HDSizeSel=|ENVI &&HDModelSel=|ENVI &&FlagUI=0|ENVI &&KillVD=0|ENVI &&CGIDirESDList=|ENVI &&CGIDirLevel=0
TEAM ENVI &&SHUTorREBOOT=0|ENVI &&DynOSVolume=|ENVI &&DynCopy=0|ENVI &&DrvLettBackup=|ENVI &&SRCDrvLett=|ENVI &&DSTDrvLett=
TEAM ENVI &&SystemNumber=|ENVI &&BackupNum=|ENVI &&SysDrvNum=|ENVI &&SysPartNum=|ENVI &&BKDefaultPath=|ENVI &&BKPARTDRV=
TEAM ENVI &&pBusType=0|ENVI &&PartCPYNoIDE=|ENVI &&hBusType=0|ENVI &&HDCPYNoIDE=|ENVI &&PESysDrv=|ENVI &&OKSysDrv=|ENVI &&I=0
TEAM ENVI &&SYSVERSION=0|ENVI &&VERNUM=|ENVI &&FromConfig=0|ENVI &&CGIEXEDir=|ENVI &&CGIDirGHOList=|ENVI &&CGIDirGHO=|ENVI &&CGIDirWIMList=
TEAM ENVI &&BGHOPATH=|ENVI &&FullPath=|ENVI &&KillGHOFlag=0|ENVI &&OldGHOExist=0|ENVI &&OldGHOTime=0|ENVI &&CheckGHOTime=0
REGI $HKLM\SYSTEM\CurrentControlSet\Control\SystemStartOptions,&&PEorNOT
LPOS* &PEPOS=minint,1,%&PEorNOT%
SHOW =1 &
CALL @MHGHO2012
IFEX $%&KillVD%=1,CALL DoVirtualDrive
IFEX $%&SHUTorREBOOT%=1,CALL MyPowerOff
IFEX $%&SHUTorREBOOT%=2,CALL MyRestart
TEAM ENVI &vFORM=|ENVI &LnvFORM=|ENVI &PARTSEL1=|ENVI &PARTSEL2=|ENVI &PARTSEL5=
TEAM ENVI &P2PList=|ENVI &FFDrv=||ENVI$ &NLDD=|ENVI$ &NLHH=|ENVI$ &TAB=|ENVI &GinCD=|ENVI &ahCHECK=|ENVI &PEPOS=
TEAM ENVI &HDMHINFO=|ENVI &HDSEL=|ENVI &HDLIST=|ENVI &IsWOW64=|ENVI &PLIST1ITEM=|ENVI &DLIST1ITEM=|ENVI &ILIST1ITEM=
TEAM ENVI &HDSizeSel=|ENVI &HDModelSel=|ENVI &FlagUI=|ENVI &KillVD=|ENVI &CGIDirESDList=|ENVI &CGIDirLevel=
TEAM ENVI &SHUTorREBOOT=|ENVI &DynOSVolume=|ENVI &DynCopy=|ENVI &DrvLettBackup=|ENVI &SRCDrvLett=|ENVI &DSTDrvLett=
TEAM ENVI &SystemNumber=|ENVI &BackupNum=|ENVI &SysDrvNum=|ENVI &SysPartNum=|ENVI &BKDefaultPath=|ENVI &BKPARTDRV=
TEAM ENVI &pBusType=|ENVI &PartCPYNoIDE=|ENVI &hBusType=|ENVI &HDCPYNoIDE=|ENVI &PESysDrv=|ENVI &OKSysDrv=|ENVI &I=
TEAM ENVI &SYSVERSION=|ENVI &VERNUM=|ENVI &FromConfig=|ENVI &CGIEXEDir=|ENVI &CGIDirGHOList=|ENVI &CGIDirGHO=|ENVI &CGIDirWIMList=
TEAM ENVI &BGHOPATH=|ENVI &FullPath=|ENVI &KillGHOFlag=|ENVI &OldGHOExist=|ENVI &OldGHOTime=|ENVI &CheckGHOTime=|ENVI &CheckGHOSize=

_SUB DoVirtualDrive
    EXEC =*ImDisk.exe -D -m %&FFDrv%: 
_END

_SUB MyPowerOff
    IFEX $%&PEPOS%=0,EXEC shutdown.exe /s /t 0!%SystemRoot%\System32\PECMD.EXE SHUT
    WAIT 3000
    SHUT
    WAIT 5000
    SHUT SHUTDOWN -s
_END

_SUB MyRestart
    IFEX $%&PEPOS%=0,EXEC shutdown.exe /r /t 0!%SystemRoot%\System32\PECMD.EXE SHUT R
    WAIT 3000
    SHUT R
    WAIT 5000
    SHUT SHUTDOWN -r
_END

_SUB Page1,W472H376,P1,,,#
    ENVI &&TITLE=+40:序号%&TAB%+40:盘符%&TAB%=65:总大小%&TAB%=70:可用空间%&TAB%+70:分区类型%&TAB%+70:文件系统%&TAB%80:  卷标
    GROU GHOGROU1,L10T6W454H60
    LABE REBK,L18T20W440H18,1.请选择您要进行的操作：
    RADI RERADI,L34T40W110H20,还原分区,CALL MAKEVIS1,1
    RADI BKRADI,L152T40W110H20,备份分区,CALL MAKEVIS2,0
    RADI PART2PART,L268T40W110H20,分区对拷,CALL MAKEVIS3,0
    GROU GHOGROU2,L10T68W454H140
    LABE PLABE,L18T82W250H18,2.请选择分区（用鼠标左键单击）
    LABE -left ShowSysDrv,L270T82W190H18,,,0xFF0000
    TABL GHOSTABL,L18T100W435H100,%&TITLE%,,0x100c0   
    GROU GHOGROU3,L10T210W454H58
    LABE RETIP,L18T224W240H16,3.请选择镜像文件：
    LIST -h GHOLIST,L18T240W415H200,,TEAM ENVI. @STATUS3=所选路径/文件：%GHOLIST%|CALL WIMGICHECK "%GHOLIST%",,0x10100   
    ITEM ReBUTTON,L435T240W25H20,...,CALL RESPATH
    LIST GHOBACK,L18T240W415H20,,ENVI. @STATUS3=所选路径/文件：%GHOBACK%,,0x10114
    ITEM BkBUTTON,L435T240W25H20,...,CALL BACKPATH,,16
    EDIT+ INFO01,L22T244W360H15,,,
    LIST SPART,L30T240W140H20,,CALL SetSTATUS4,,0x110
    LABE DLABLE,L260T224W200H16,3.请选择目标分区：
    ENVI @DLABLE.Visable=0
    LIST DPART,L272T240W140H20,,CALL SetSTATUS5,,0x110
    GROU GHOGROU4,L10T270W454H116
    LABE STATUS0,L18T284W100H18,状态：
    LABE -left STATUS1,L30T304W420H18,所选操作：还原分区,,0xFF0000
    LABE -left STATUS2,L30T324W420H18,所选分区：无,,0xFF0000
    LABE -left STATUS4,L30T324W420H18,源分区：无,,0xFF0000
    ENVI @STATUS4.Visable=0
    LABE. -left STATUS3,L30T344W420H38,所选路径/文件：无,,0xFF0000
    LABE -left STATUS5,L30T344W420H18,目标分区：无,,0xFF0000
    ENVI @STATUS5.Visable=0
_END

_SUB Page2,W472H376,P2,,,#
    ENVI &&hTITLE=+80:磁盘序号%&TAB%+95:磁盘容量%&TAB%280:   厂商和型号
    GROU hGROU1,L10T6W454H60
    LABE hREBK,L18T20W440H18,1.请选择您要进行的操作：
    RADI hRERADI,L34T40W110H20,还原硬盘,CALL HDVIS1,0
    RADI hBKRADI,L152T40W110H20,备份硬盘,CALL HDVIS2,0
    RADI HD2HD,L268T40W110H20,硬盘对拷,CALL HDVIS3,0
    GROU hGROU2,L10T68W454H140
    LABE hLABE,L18T82W440H18,2.请选择硬盘（用鼠标左键单击）：
    TABL hTABL,L18T100W440H100,%&hTITLE%,,0x100c0
    LIST -h hLIST,L18T240W415H160,    ,TEAM ENVI. @hSTATUS3=所选路径/文件：%hLIST%|ENVI &ahCHECK=2|CALL GICHECK "%hLIST%",,0x10100
    GROU hGROU3,L10T210W454H58
    LABE hRETIP,L18T224W240H16,3.请选择镜像文件：
    ITEM hReBn,L435T240W25H20,...,CALL hRESPATH
    LIST hBACK,L18T240W415H20,D:\SYSTEM.GHO,ENVI. @hSTATUS3=所选路径/文件：%hBACK%,D:\SYSTEM.GHO,0x10114
    ITEM hBkBn,L435T240W25H20,...,CALL hBACKPATH,,16
    EDIT+ hINFO01,L22T244W360H15,,,
    LIST SRCHD,L30T240W140H20,,CALL SethSTATUS4,,0x110
    LABE hLABLE,L260T224W200H16,3.请选择目标硬盘：
    ENVI @hLABLE.Visable=0
    LIST DSTHD,L272T240W140H20,,CALL SethSTATUS5,,0x110
    GROU hGROU4,L10T270W454H116
    LABE hSTATUS0,L18T284W100H18,状态：
    LABE -left hSTATUS1,L30T304W420H18,所选操作：无,,0xFF0000
    LABE -left hSTATUS2,L30T324W420H18,所选硬盘：无,,0xFF0000
    LABE -left hSTATUS4,L30T324W420H18,源硬盘：无,,0xFF0000
    ENVI @hSTATUS4.Visable=0
    LABE. -left hSTATUS3,L30T344W420H38,所选路径/文件：无,,0xFF0000
    LABE -left hSTATUS5,L30T344W420H18,目标硬盘：无,,0xFF0000
    ENVI @hSTATUS5.Visable=0
_END

_SUB Page3,W472H376,P3,,,#
    GROU ,L10T7W454H190,参数设置,
    CHEK advIDE,L22T34W166H18,禁用访问IDE设备,,1
    CHEK advPWD1,L202T34W52H18,密码,CALL EnablePWD,0
    EDIT advEDIT1,L255T33W120H18,,,-
    LABE ,L18T76W61H18,还原时：,,
    CHEK advCRC,L80T73W368H18,忽略CRC错误,,0
    LABE ,L18T116W61H18,备份时：,,
    LIST advBL01,L80T112W90H18,不压缩|快速压缩|高压缩|极限压缩,,极限压缩,
    LIST advBL02,L206T112W80H18,不分卷|650 MB|1950 MB|3950 MB|自动检测,,不分卷,
    CHEK HideFolder,L318T112W140H18,隐藏备份文件夹,,0
    LABE ,L18T165W80H18,其它参数：,,
    EDIT paras,L100T161W286H18,,,
    ITEM ,L390T157W70H25,帮 助,ENVI @-.POSTMSG=#4;3;0,
    GROU ,L10T206W454H93,检查GHO镜像的完整性,
    LIST -h advLIST,L18T227W414H170,,TEAM ENVI. @advLABE=所选文件：%advLIST%|ENVI &ahCHECK=3|CALL GICHECK "%advLIST%",,0x10100
    ITEM advBn1,L434T227W25H20,...,CALL advPATH,
    LABE. -left advLABE,L18T254W360H32,所选文件：,,0xFF0000,
    ITEM advBn2,L380T265W80H28,开始检查,CALL IntegCheck,
_END

_SUB MHGHO2012,W502H500,CGI 4.0.3.3,,#1,
    TABS TABS1,L10T6W476H416,Page1:PARTMH:操作分区:对分区进行操作;Page2:HDMH:操作硬盘:对整个硬盘进行操作;Page3:ADVANMH:高 级:其它参数设置和功能,
    LABE -left WIMVER,L20T427W230H16,ImageX64: v10.0.14393,
    LABE -left GHOVER,L20T446W230H16,Ghost64: v12.0.0.10531,
    ITEM DOIT1,L328T430W70H28,执 行,CALL DOITph,
    ITEM DOIT2,L406T430W70H28,关 闭,KILL \,
    ENVI @TABS1.MSG=_%WM_LBUTTONDOWN%: CALL OnLButton_TABS1
    TEAM ENVI &&GHOLS=|ENVI &&GHOLS1=|ENVI &&WIMLS=|ENVI &&ESDLS=|ENVI &&ISOLS=
    TEAM ENVI &&wp=|ENVI &&lp=|ENVI &&J=0|ENVI &&BasicDone=0|ENVI &&DL=  
    ENVI @PARTMH:GHOSTABL.MSG=_%&WM_LBUTTONDOWN%:   CALL GHOSTCHECK
    ENVI @PARTMH:GHOSTABL.MSG=_%&WM_LBUTTONDBLCLK%:  CALL OPENPART
    ENVI @HDMH:hTABL.MSG=_%&WM_LBUTTONDOWN%:  CALL HDCHECK   
    ENVI @PARTMH:STATUS3.MSG=%&WM_MOUSEHOVER%:   CALL DISPTIP 1
    ENVI @HDMH:hSTATUS3.MSG=%&WM_MOUSEHOVER%:  CALL DISPTIP 2
    ENVI @ADVANMH:advLABE.MSG=%&WM_MOUSEHOVER%:  CALL DISPTIP 3
    ENVI @PARTMH:STATUS3.MSG=%&WM_MOUSELEAVE%:  TIPS -
    ENVI @HDMH:hSTATUS3.MSG=%&WM_MOUSELEAVE%:  TIPS -
    ENVI @ADVANMH:advLABE.MSG=%&WM_MOUSELEAVE%:  TIPS -
    ENVI @MHGHO2012.MSG=#1: CALL OnMsg1
    TIME Timer1,1000, CALL OnTimer1
    CALL OnTimer1
    THREAD*  GODRVINFO
    TIME &KillGHOTimer,0, CALL OnKillGHOTimer
    ENVI @this.MSG=_#4: CALL @*paraHELP
_END

_SUB OPENPART
    ENVI  @GHOSTABL.Sel=?&&Sel
    ENVI  @GHOSTABL.Val=?%&Sel%.2;&&P4VIEW
    FIND $%&P4VIEW%=  ,! EXEC !CMD.EXE /C START "" %&P4VIEW%\
_END

_SUB OnLButton_TABS1
    FIND $%&TABS1.Select%=3,TEAM ENVI @DOIT1.Enable=0|ENVI @DOIT2.Visable=1
    FIND $%&TABS1.Select%=1,
    {
        ENVI @DOIT1.Enable=1
        ENVI @DOIT2.Visable=1       
        FIND $%PART2PART.Check%=1, CALL PARTCOPYNOIDE2! CALL SetNOIDE3
    }
    FIND $%&TABS1.Select%=2,
    {
        ENVI @DOIT1.Enable=1
        ENVI @DOIT2.Visable=1
        FIND $%HD2HD.Check%=1, CALL SetHDCOPYIDE2! CALL SetHDIDE2
    }
_END

_SUB GODRVINFO
    ENVI &CGIEXEDir=%CurDir%
    CALL GetCGIDirLevel
    EXEC* -exe:#600 &vFORM=!USORT.EXE -mohong
    EXEC* -exe:#601 &HDMHINFO=!HDSIZEID.EXE -mohong
    ENVI @PARTMH:GHOSTABL.Val=1*;%&vFORM%
    ENVI @HDMH:hTABL.Val=1*;%&HDMHINFO%
    CALL FINDGHO
    CALL FINDWIM
    CALL FINDESD
    CALL FINDISO
    CALL FINDGHOInCGIDir
    CALL FINDWIMInCGIDir
    CALL FINDESDInCGIDir
    ENVI @Timer1=0
    ENVI @MHGHO2012.POSTMSG=#1
_END

_SUB GetCGIDirLevel
    TEAM ENVI &&M=1|ENVI &&iPOS=0
    LOOP 1,
    {
        LPOS &iPOS=\,%&M%,%&CGIEXEDir%
        IFEX $%&iPOS% = 0, EXIT LOOP
        CALC #&CGIDirLevel = %&CGIDirLevel% + 1
        CALC #&M = %&M% + 1
    }
_END

_SUB OnMsg1
    CALL SetDiskInfo    
    CALL SetSizeHiddenPart
    IFEX $%&PEPOS% = 0, TEAM ENVI @PARTMH:ShowSysDrv=（系统盘为 %SYSTEMDRIVE% 盘）|ENVI &OKSysDrv=%SYSTEMDRIVE%|CALL SetBackupPath! CALL FindPEWINDRV
    TEAM ENVI @Timer1=0| ENVI @PARTMH:INFO01.Visable=0| ENVI @HDMH:hINFO01.Visable=0
    TEAM ENVI @PARTMH:GHOLIST.VAL=%&GHOLS%|ENVI @HDMH:hLIST.VAL=%&GHOLS%|ENVI @ADVANMH:advLIST.VAL=%&GHOLS%
    FIND $%&BKDefaultPath% = ,! ENVI &GHOLS1=%&BKDefaultPath% 
    FIND $%&CGIDirGHO%=,!
    {
        IFEX $%&CGIDirLevel% > 1, TEAM ENVI @PARTMH:GHOLIST.ADD=%&CGIDirGHOList%|ENVI @HDMH:hLIST.ADD=%&CGIDirGHOList%|ENVI @ADVANMH:advLIST.ADD=%&CGIDirGHOList%
        ENVI &GHOLS1=%&CGIDirGHO%
    }
    ENVI @PARTMH:GHOLIST.SEL=%&GHOLS1%
    FIND $%BKRADI.Check%=0,!! FIND $%PART2PART.Check%=0,!! ENVI. @PARTMH:STATUS3=所选路径/文件：%&GHOLS1%
    ENVI @HDMH:hLIST.SEL=%&GHOLS1%
    FIND $%hBKRADI.Check%=0,!! FIND $%HD2HD.Check%=0,!! ENVI. @HDMH:hSTATUS3=所选路径/文件：%&GHOLS1%   
    ENVI @ADVANMH:advLIST.SEL=%&GHOLS1%
    ENVI. @ADVANMH:advLABE=所选文件：%&GHOLS1%
    ENVI @PARTMH:GHOLIST.ADD=%&WIMLS%
    FIND $%&CGIDirWIMList%=,!
    {
        IFEX $%&CGIDirLevel% > 1, ENVI @PARTMH:GHOLIST.ADD=%&CGIDirWIMList%
    }
    ENVI @PARTMH:GHOLIST.ADD=%&ESDLS%
    FIND $%&CGIDirESDList%=,!
    {
        IFEX $%&CGIDirLevel% > 1, ENVI @PARTMH:GHOLIST.ADD=%&CGIDirESDList%
    }
    TEAM ENVI @PARTMH:GHOLIST.ADD=%&ISOLS%|ENVI @HDMH:hLIST.ADD=%&ISOLS%|ENVI @ADVANMH:advLIST.ADD=%&ISOLS%
    FIND $%&OKSysDrv%=,! CALL SelectSystemInTBAL
    ENVI @PARTMH:GHOLIST.QUERY=&&AllItems
    FIND $%&AllItems%=,!
    {
        ENVI @PARTMH:GHOLIST.QUERY=1;&PLIST1ITEM
        ENVI @HDMH:hLIST.QUERY=1;&DLIST1ITEM
        ENVI @ADVANMH:advLIST.QUERY=1;&ILIST1ITEM
    }
    CALL GetSystemVersion
    ENVI &BasicDone=1 
_END

_SUB SetBackupPath
    TEAM ENVI &&faultPath=|ENVI &&fDrive=|ENVI &&vLn=|ENVI &&A2=|ENVI &&A5=|ENVI &&A6=|ENVI &&A9=|ENVI &&YinCA=
    FORX *ab \SYBACKUP\RESC.GHO,&faultPath,1,
    { 
      FIND %&faultPath%=,!
      {
       FDRV &fDrive=%&faultPath%
       ENVI @PARTMH:GHOBACK.ADD=%&fDrive%\SYSTEM.GHO
       TEAM ENVI @PARTMH:GHOBACK.ADDSEL=%&faultPath%|ENVI &BKDefaultPath=%&faultPath%
       ENVI @PARTMH:GHOBACK.ADD=%&fDrive%\SYSTEM.WIM
       ENVI @PARTMH:GHOBACK.ADD=%&fDrive%\SYBACKUP\RESC.WIM
       ENVI @PARTMH:GHOBACK.ADD=%&fDrive%\SYSTEM.ESD
       ENVI @PARTMH:GHOBACK.ADD=%&fDrive%\SYBACKUP\RESC.ESD
       EXIT _SUB
      }         
    }
    FIND $%&faultPath%=,!!
    {
      FORX *NL &vFORM,&vLn,
       {
         MSTR* &A2,&A5,&A6,&A9=<2><5><6><9>%&vLn%
         LSTR &YinCA=6,%&A6%
         FIND $%&A2%<>%&OKSysDrv%,!! FIND $%&A5%<>EFI,!! FIND $%&YinCA%<>hidden,!! FIND $%&A9%<>1,!! TEAM ENVI &BKPARTDRV=%&A2%|EXIT FORX 
       }
      FIND %&BKPARTDRV%=,!
       {
         ENVI @PARTMH:GHOBACK.ADD=%&BKPARTDRV%\SYSTEM.GHO
         ENVI @PARTMH:GHOBACK.ADDSEL=%&BKPARTDRV%\SYBACKUP\RESC.GHO
         ENVI @PARTMH:GHOBACK.ADD=%&BKPARTDRV%\SYSTEM.WIM
         ENVI @PARTMH:GHOBACK.ADD=%&BKPARTDRV%\SYBACKUP\RESC.WIM
         ENVI @PARTMH:GHOBACK.ADD=%&BKPARTDRV%\SYSTEM.ESD
         ENVI @PARTMH:GHOBACK.ADD=%&BKPARTDRV%\SYBACKUP\RESC.ESD        
       }
    }  
_END

_SUB FindPEWINDRV
    CALL GetSysDrvInPE
    FIND $%&PESysDrv%=, EXIT _SUB
    ENVI @PARTMH:ShowSysDrv=（系统盘为%&PESysDrv%盘）
    ENVI &OKSysDrv=%&PESysDrv%
    CALL SetBackupPath %&PESysDrv%
_END

_SUB GetAnyDrvNumByDrvLett
    TEAM ENVI &&vln=|ENVI &&A1=|ENVI &&A2=|ENVI &&iPOS=
    ENVI &&DrvLett=%1
    ENVI &AnyDrvNum=0
    FORX *NL &vFORM,&vln,
    {
        MSTR* &A1,&A2=<1><2>%&vln%
        FIND $%&A2%=%&DrvLett%,!!
        {
            LPOS &iPOS=:,1,%&A1%
            CALC #&iPOS = %&iPOS% - 1
            LSTR &AnyDrvNum=%&iPOS%,%&A1%
            EXIT _SUB
        }
    }
_END

_SUB GetAnyBusTypeByDrvNum
    TEAM ENVI &&vln=|ENVI &&A1=|ENVI &&A4=
    ENVI &&HDNumber=%1
    ENVI &AnyBusType=0
    FORX *NL &HDMHINFO,&vln,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&HDNumber%, TEAM ENVI &AnyBusType=%&A4%|EXIT _SUB
    }
_END

_SUB GetSysDrvInPE
    TEAM ENVI &&vd=|ENVI &&A1=|ENVI &&A2=|ENVI &&A9=|ENVI &&vln=|ENVI &&szNUM=|ENVI &&iPOS=0
    TEAM ENVI &&HD1DrvList=|ENVI &&HD2DrvList=|ENVI &&DrvList=|ENVI &&AnyDrvNum=0|ENVI &&XDrvNum=
    CALL GetAnyDrvNumByDrvLett %SYSTEMDRIVE%
    ENVI &XDrvNum=%&AnyDrvNum%
    IFEX $%&XDrvNum%=1,!
    {
        CALL GetAllDrvLettOnDrive 1
        ENVI &HD1DrvList=%&DrvList%
        FORX * %&HD1DrvList%,&vd,
        {
            IFEX %&vd%\Windows, TEAM ENVI &PESysDrv=%&vd%|ENVI &SysDrvNum=1| EXIT FORX
        }
        FIND $%&PESysDrv%=,! EXIT _SUB
    }
    IFEX $%&XDrvNum%=2,!
    {
        CALL GetAllDrvLettOnDrive 2
        ENVI &HD2DrvList=%&DrvList%
        FORX * %&HD2DrvList%,&vd,
        {
            IFEX %&vd%\Windows, TEAM ENVI &PESysDrv=%&vd%|ENVI &SysDrvNum=2| EXIT FORX
        }
        FIND $%&PESysDrv%=,! EXIT _SUB
    }
    // ======== GPT SSD 需考虑， 结合活动分区、总线类型 =======================
    TEAM ENVI &&PTStyleHD1=|ENVI &&PTStyleHD2=|ENVI &&PTStyleHD=|ENVI &&ActPartDrv=
    CALL GetPartitionTableStyle 1
    ENVI &PTStyleHD1=%&PTStyleHD%
    CALL GetPartitionTableStyle 2
    ENVI &PTStyleHD2=%&PTStyleHD%
    TEAM ENVI &&szHD1=|ENVI &&szHD2=|ENVI &&szHD=
    CALL CheckIsSSD 1
    ENVI &szHD1=%&szHD%
    CALL CheckIsSSD 2
    ENVI &szHD2=%&szHD%
    TEAM ENVI &&ESPExist=0|ENVI &&vSSD=0
    LPOS* &vSSD=SSD,1,%&szHD1%
    IFEX $%&vSSD% > 0,
    {
        FIND $%&PTStyleHD1%=MBR,
        {
            CALL ActivePartitionDrv 1
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD1%=GPT,
        {
            CALL CheckESP 1
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 1
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    ENVI &vSSD=0
    LPOS* &vSSD=SSD,1,%&szHD2%
    IFEX $%&vSSD% > 0,
    {
        FIND $%&PTStyleHD2%=MBR,
        {
            CALL ActivePartitionDrv 2
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD2%=GPT,
        {
            CALL CheckESP 2
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 2
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    TEAM ENVI &&BusTypeHD1=0|ENVI &&BusTypeHD2=0|ENVI &&AnyBusType=0|ENVI &&BTHD1=Y|ENVI &&BTHD2=Y
    CALL GetAnyBusTypeByDrvNum 1
    ENVI &BusTypeHD1=%&AnyBusType%
    CALL GetAnyBusTypeByDrvNum 2
    ENVI &BusTypeHD2=%&AnyBusType%
    IFEX $%&BusTypeHD1% = 7, ENVI &BTHD1=NonHD
    IFEX $%&BusTypeHD1% = 0, ENVI &BTHD1=NonHD
    IFEX $%&BusTypeHD2% = 7, ENVI &BTHD2=NonHD
    IFEX $%&BusTypeHD2% = 0, ENVI &BTHD2=NonHD
    FIND $%&BTHD1%=Y,
    {
        FIND $%&PTStyleHD1%=MBR,
        {
            CALL ActivePartitionDrv 1
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD1%=GPT,
        {
            CALL CheckESP 1
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 1
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    FIND $%&BTHD2%=Y,
    {
        FIND $%&PTStyleHD2%=MBR,
        {
            CALL ActivePartitionDrv 2
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD2%=GPT,
        {
            CALL CheckESP 2
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 2
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    // 如果搜不到，再按以上规则搜第三、第四块硬盘===============
    ENVI &&HD3DrvList=
    IFEX $%&XDrvNum%=3,!
    {
        CALL GetAllDrvLettOnDrive 3
        ENVI &HD3DrvList=%&DrvList%
        FORX * %&HD3DrvList%,&vd,
        {
            IFEX %&vd%\Windows, TEAM ENVI &PESysDrv=%&vd%|ENVI &SysDrvNum=3| EXIT FORX
        }
        FIND $%&PESysDrv%=,! EXIT _SUB
    }
    ENVI &&HD4DrvList=
    IFEX $%&XDrvNum%=4,!
    {
        CALL GetAllDrvLettOnDrive 4
        ENVI &HD4DrvList=%&DrvList%
        FORX * %&HD4DrvList%,&vd,
        {
            IFEX %&vd%\Windows, TEAM ENVI &PESysDrv=%&vd%|ENVI &SysDrvNum=4| EXIT FORX
        }
        FIND $%&PESysDrv%=,! EXIT _SUB
    }
    TEAM ENVI &&PTStyleHD3=|ENVI &&PTStyleHD4=
    CALL GetPartitionTableStyle 3
    ENVI &PTStyleHD3=%&PTStyleHD%
    CALL GetPartitionTableStyle 4
    ENVI &PTStyleHD4=%&PTStyleHD%
    TEAM ENVI &&szHD3=|ENVI &&szHD4=
    CALL CheckIsSSD 3
    ENVI &szHD3=%&szHD%
    CALL CheckIsSSD 4
    ENVI &szHD4=%&szHD%
    ENVI &vSSD=0
    LPOS* &vSSD=SSD,1,%&szHD3%
    IFEX $%&vSSD% > 0,
    {
        FIND $%&PTStyleHD3%=MBR,
        {
            CALL ActivePartitionDrv 3
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD3%=GPT,
        {
            CALL CheckESP 3
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 3
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    ENVI &vSSD=0
    LPOS* &vSSD=SSD,1,%&szHD4%
    IFEX $%&vSSD% > 0,
    {
        FIND $%&PTStyleHD4%=MBR,
        {
            CALL ActivePartitionDrv 4
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD2%=GPT,
        {
            CALL CheckESP 4
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 4
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    TEAM ENVI &&BusTypeHD3=0|ENVI &&BusTypeHD4=0|ENVI &&BTHD3=Y|ENVI &&BTHD4=Y
    CALL GetAnyBusTypeByDrvNum 3
    ENVI &BusTypeHD3=%&AnyBusType%
    CALL GetAnyBusTypeByDrvNum 4
    ENVI &BusTypeHD4=%&AnyBusType%
    IFEX $%&BusTypeHD3% = 7, ENVI &BTHD3=NonHD
    IFEX $%&BusTypeHD3% = 0, ENVI &BTHD3=NonHD
    IFEX $%&BusTypeHD4% = 7, ENVI &BTHD4=NonHD
    IFEX $%&BusTypeHD4% = 0, ENVI &BTHD4=NonHD
    FIND $%&BTHD3%=Y,
    {
        FIND $%&PTStyleHD3%=MBR,
        {
            CALL ActivePartitionDrv 3
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD3%=GPT,
        {
            CALL CheckESP 3
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 3
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
    FIND $%&BTHD4%=Y,
    {
        FIND $%&PTStyleHD4%=MBR,
        {
            CALL ActivePartitionDrv 4
            FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
        }
        FIND $%&PTStyleHD4%=GPT,
        {
            CALL CheckESP 4
            FIND $%&ESPExist%=1,
            {
                CALL FirstNTFSPartition 4
                FIND $%&ActPartDrv%=,! TEAM ENVI &PESysDrv=%&ActPartDrv%|EXIT _SUB
            }
        }
    }
_END

_SUB GetPartitionTableStyle
    TEAM ENVI &&vln=|ENVI &&A1=|ENVI &&A8=|ENVI &&E1=|ENVI &&E2=
    ENVI &&HDNumber=%1
    ENVI &PTStyleHD=
    FORX *NL &vFORM,&vln,
    {
        MSTR* &A1,&A8=<1><8>%&vln%
        LPOS &E1=:,1,%&A1%
        CALC #&E1 = %&E1% - 1
        LSTR &E2=%&E1%,%&A1%
        IFEX $%&E2% = %&HDNumber%, TEAM ENVI &PTStyleHD=%&A8%|EXIT _SUB
    }
_END

_SUB CheckIsSSD
    TEAM ENVI &&vln=|ENVI &&A1=|ENVI &&A5=
    ENVI &&HDNumber=%1
    ENVI &szHD=
    FORX *NL &HDMHINFO,&vln,
    {
        MSTR* &A1,&A5=<1><5>%&vLn%
        FIND $%&A1%=%&HDNumber%, TEAM ENVI &szHD=%&A5%|EXIT _SUB
    }
_END

_SUB ActivePartitionDrv
    TEAM ENVI &&vln=|ENVI &&A1=|ENVI &&A2=|ENVI &&A9=|ENVI &&E1=|ENVI &&E2=
    ENVI &&HDNumber=%1
    ENVI &ActPartDrv=
    FORX *NL &vFORM,&vln,
    {
        MSTR* &A1,&A2,&A9=<1><2><9>%&vln%
        IFEX $%&A9% = 1,
        {
            LPOS &E1=:,1,%&A1%
            CALC #&E1 = %&E1% - 1
            LSTR &E2=%&E1%,%&A1%
            IFEX $%&E2% = %&HDNumber%,!! FIND $%&A2%=%SYSTEMDRIVE%,! TEAM ENVI &ActPartDrv=%&A2%|EXIT _SUB
        }
    }
_END

_SUB CheckESP
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A5=|ENVI &&tPOS=|ENVI &&aNum=
    ENVI &&HDNumber=%1
    ENVI &ESPExist=0
    FORX *NL &vFORM,&vLn,
    {
        MSTR* &A1,&A5=<1><5>%&vLn%
        FIND $%&A5%=EFI,
        {
            LPOS &tPOS=:,1,%&A1%
            CALC #&tPOS = %&tPOS% - 1
            LSTR &aNum=%&tPOS%,%&A1%
            IFEX $%&aNum% = %&HDNumber%, TEAM ENVI &ESPExist=1|EXIT _SUB
        }
    }
_END

_SUB FirstNTFSPartition
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A2=|ENVI &&A6=|ENVI &&tPOS=|ENVI &&aNum=
    ENVI &&HDNumber=%1
    ENVI &ActPartDrv=
    FORX *NL &vFORM,&vLn,
    {
        MSTR* &A1,&A2,&A6=<1><2><6>%&vLn%
        FIND $%&A6%=NTFS,
        {
            LPOS &tPOS=:,1,%&A1%
            CALC #&tPOS = %&tPOS% - 1
            LSTR &aNum=%&tPOS%,%&A1%
            IFEX $%&aNum% = %&HDNumber%,
            {
                FIND $%&A2%=%SYSTEMDRIVE%,! ENVI &ActPartDrv=%&A2%
                FIND $%&ActPartDrv%=,! EXIT _SUB
            }
        }
    }
_END

_SUB SelectSystemInTBAL
    TEAM ENVI &&M=1| ENVI &&FTDRV=| ENVI &&SysLine=
    LOOP #%&M% <= %&LnvFORM%,
    {
        ENVI @PARTMH:GHOSTABL.Val=?%&M%.2;&FTDRV
        FIND $%&FTDRV%=%&OKSysDrv%, TEAM ENVI @PARTMH:GHOSTABL.Sel=%&M%|EXIT LOOP
        CALC #&M = %&M% + 1
    }
    ENVI  @PARTMH:GHOSTABL.Val=?%&M%.1;&PARTSEL1
    ENVI  &PARTSEL2=%&OKSysDrv%
    ENVI  @PARTMH:GHOSTABL.Val=?%&M%.5;&PARTSEL5
    ENVI &DrvLettBackup=%&PARTSEL2%   
    FIND $%&PARTSEL2%=  ,ENVI @PARTMH:STATUS2=所选分区：  序号 %&PARTSEL1%         无盘符!ENVI @PARTMH:STATUS2=所选分区：  序号 %&PARTSEL1%         盘符 %&PARTSEL2%
    CALL SetNOIDE3
_END

_SUB GetSystemVersion
    ENVI &&WINVER=
    EXEC*- &&line=!CMD.EXE /C ver
    RPOS &&szPOS=[,1,%&line%
    MSTR &&tString=%&szPOS%,0,%&line%
    MSTR &WINVER=<2>%&tString%
    LPOS &&aSysPOS=.,1,%&WINVER%
    CALC #&aSysPOS = %&aSysPOS% - 1
    LSTR &SYSVERSION=%&aSysPOS%,%&WINVER%
    LPOS &&VerPOS=.,2,%&WINVER%
    CALC #&VerPOS = %&VerPOS% - 1
    LSTR &VERNUM=%&VerPOS%,%&WINVER%
_END

//=========================================== 初始化结束 =========================================================================
_SUB GetOSVolume
    FILE GHSTSTAT.TXT
    EXEC* -exe:#200 =!ghost.exe -dd
    EXEC* -exe:#602 &DynOSVolume=!OSVOLNumber.exe
    FILE GHSTSTAT.TXT
    FILE ghost*.dmp
_END

_SUB GetNumberOfVolume
    CALL GetOSVolume
    FIND $%&DynOSVolume%=,EXIT _SUB
    TEAM ENVI &&V1=|ENVI &&V2=|ENVI &&DynVol=
    FORX *NL &DynOSVolume,&DynVol,
    {
         MSTR &V1,&V2=<1><2>%&DynVol%
         FIND $%&V2%=%&PARTSEL2%, TEAM ENVI &PARTSEL1=%&V1%|EXIT FORX
    }
_END

_SUB SetSizeHiddenPart
    READ -,-1,&LnvFORM,%&vFORM%
    TEAM ENVI &&M=1| ENVI &&FTDRV=| ENVI &&HIDDEN=| ENVI &&F8=
    TEAM ENVI &&PartNo=| ENVI &&DrvLett=
    LOOP #%&M% <= %&LnvFORM%,
    {
      ENVI @PARTMH:GHOSTABL.Val=?%&M%.6;&FTDRV
      LSTR &HIDDEN=7,%&FTDRV%
	    MSTR &F8=8,0,%&FTDRV%
      FIND $%&HIDDEN%=hidden_, TEAM ENVI @PARTMH:GHOSTABL.Color=*%&M%;0xFF| ENVI @PARTMH:GHOSTABL.Val=%&M%.6;隐藏%&F8%
      ENVI @PARTMH:GHOSTABL.Val=?%&M%.1;&PartNo
      ENVI @PARTMH:GHOSTABL.Val=?%&M%.2;&DrvLett
      FIND $%&PartNo%=, ENVI &P2PList=%&P2PList%           %&DrvLett%%NLDD%! ENVI &P2PList=%&P2PList%  %&PartNo%      %&DrvLett%%NLDD%
      CALC #&M = %&M% + 1
    }
    // 设置【分区对拷】下拉框
    ENVI @PARTMH:SPART.ADD=%&P2PList%
    ENVI @PARTMH:DPART.ADD=%&P2PList%
    // 在Native PE 中，winvblock模拟的盘被识别为Fixed HD（GHOST32也是如此），需除去其分区。
    IFEX $%&PEPOS% > 0,
    {
        TEAM ENVI &M=1| ENVI &&HDNumberX=
        LOOP #%&M% <= %&LnvFORM%,
        {
            ENVI @PARTMH:GHOSTABL.Val=?%&M%.2;&DrvLett
            FIND $%&DrvLett%=%SYSTEMDRIVE%,
            {
                ENVI @PARTMH:GHOSTABL.Val=?%&M%.1;&HDNumberX
                ENVI @PARTMH:GHOSTABL.Val=-%&M%
                // 除去【分区对拷】下拉框中相应的条目
                ENVI @PARTMH:SPART.DEL=  %&HDNumberX%      %SYSTEMDRIVE%
                ENVI @PARTMH:DPART.DEL=  %&HDNumberX%      %SYSTEMDRIVE%
                // 除去硬盘列表和【硬盘对拷】下拉框相应的条目
                CALL CutWinvblock %&HDNumberX%
                EXIT LOOP
            }
            CALC #&M = %&M% + 1
        }
    }
_END

_SUB SetDiskInfo
    READ -,-1,&&Ln,%&HDMHINFO%
    TEAM ENVI &&M=1| ENVI &&HDNumber=
    LOOP #%&M% <= %&Ln%,
    {
        ENVI @HDMH:hTABL.Val=?%&M%.1;&HDNumber
        ENVI &HDList=%&HDList%%&HDNumber%%NLDD%
        CALC #&M = %&M% + 1
    }
    // 设置【硬盘对拷】下拉框     
    ENVI @HDMH:SRCHD.ADD=%&HDList%
    ENVI @HDMH:DSTHD.ADD=%&HDList%
_END

_SUB CutWinvblock
    TEAM ENVI &&HDNumPOS=| ENVI &&hNum=| ENVI &&DiskNum=
    LPOS &HDNumPOS=:,1,%1
    CALC #&HDNumPOS = %&HDNumPOS% - 1
    LSTR &hNum=%&HDNumPOS%,%1
    READ -,-1,&&Ln,%&HDMHINFO%
        
    ENVI &M=1
    LOOP #%&M% <= %&Ln%,
    {
        ENVI @HDMH:hTABL.Val=?%&M%.1;&DiskNum
        FIND $%&DiskNum%=%&hNum%, TEAM ENVI @HDMH:hTABL.Val=-%&M%| EXIT LOOP
        CALC #&M = %&M% + 1
    }
    
    // 除去【硬盘对拷】下拉框中Native PE相应的条目
    ENVI @HDMH:SRCHD.DEL=%&hNum%
    ENVI @HDMH:DSTHD.DEL=%&hNum%
_END

_SUB GICHECK
    FEXT &&EXT=%~1
    FIND $%&EXT%=ISO,CALL F_GHOinISO %1
_END

_SUB F_GHOinISO,W420H208,ISO中GHO文件列表,,#1
    ENVI &&GITITLE=375:%~1中的GHO文件列表
    LABE ,L20T12W380H18,请选择GHO文件（用鼠标左键单击）：
    TABL GITABL,L20T32W380H100,%&GITITLE%,,0x10040
    EDIT+ GIEDIT,L50T70W340H16,,,
    ITEM GIButton1,L220T140W80H28,确 定,TEAM CALL SetSTATUS3|KILL \,
    ITEM GIButton2,L320T140W80H28,关 闭,KILL \,
    ENVI @GITABL.MSG=_%&WM_LBUTTONDOWN%:   CALL GIPICK    
    ENVI &GinCD=
    ENVI &&K=0
    ENVI &&GLSinISO=
    ENVI @F_GHOinISO.MSG=#1: CALL GIMsg1
    TIME Timer3,200, CALL OnTimer3
    CALL OnTimer3
    ENVI &&ISOPATH=%1
    THREAD* L_ISO2GHO
_END

_SUB SetSTATUS3
    FIND $%&GinCD%=,!
    {
        FIND $%&ahCHECK%=2,TEAM ENVI. @hSTATUS3=所选路径/文件：%&GinCD%|EXIT _SUB
        FIND $%&ahCHECK%=3,ENVI. @advLABE=所选文件：%&GinCD%
    }
_END

_SUB SetSTATUS4
    ENVI @STATUS4=源分区：      %SPART%
    CALL PARTCOPYNOIDE
_END

_SUB SetSTATUS5
    ENVI @STATUS5=目标分区：    %DPART%
    CALL PARTCOPYNOIDE
_END

_SUB PARTCOPYNOIDE
    FIND $%DPART%=,EXIT _SUB
    FIND $%SPART%=,EXIT _SUB
    TEAM ENVI &&S1=|ENVI &&S2=|ENVI &&IsDrv=
    MSTR &S1,&S2=<1><2>%SPART%
    RSTR &IsDrv=1,%&S1%
    FIND $%&IsDrv%=:, EXIT _SUB
    TEAM ENVI &&D1=|ENVI &&D2=
    MSTR &D1,&D2=<1><2>%DPART%
    RSTR &IsDrv=1,%&D1%
    FIND $%&IsDrv%=:, EXIT _SUB
    TEAM ENVI &&SPACOR=0|ENVI &&DrvNum=|ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=|ENVI &&IsIDE1=0|ENVI &&IsIDE2=0
    LPOS &SPACOR=:,1,%&S1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DrvNum=%&SPACOR%,%&S1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DrvNum%, TEAM ENVI &IsIDE1=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE1%=3, TEAM ENVI @-:-:-:ADVANMH:advIDE.Check=0|ENVI &PartCPYNoIDE=|EXIT _SUB
    LPOS &SPACOR=:,1,%&D1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DrvNum=%&SPACOR%,%&D1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DrvNum%, TEAM ENVI &IsIDE2=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE2%=3, TEAM ENVI @-:-:-:ADVANMH:advIDE.Check=0|ENVI &PartCPYNoIDE=|EXIT _SUB! TEAM ENVI @-:-:-:ADVANMH:advIDE.Check=1|ENVI &PartCPYNoIDE=-noide
_END

_SUB PARTCOPYNOIDE2
    FIND $%DPART%=,EXIT _SUB
    FIND $%SPART%=,EXIT _SUB
    TEAM ENVI &&S1=|ENVI &&S2=|ENVI &&IsDrv=
    MSTR &S1,&S2=<1><2>%SPART%
    RSTR &IsDrv=1,%&S1%
    FIND $%&IsDrv%=:, EXIT _SUB
    TEAM ENVI &&D1=|ENVI &&D2=
    MSTR &D1,&D2=<1><2>%DPART%
    RSTR &IsDrv=1,%&D1%
    FIND $%&IsDrv%=:, EXIT _SUB
    TEAM ENVI &&SPACOR=0|ENVI &&DrvNum=|ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=|ENVI &&IsIDE1=0|ENVI &&IsIDE2=0
    LPOS &SPACOR=:,1,%&S1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DrvNum=%&SPACOR%,%&S1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DrvNum%, TEAM ENVI &IsIDE1=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE1%=3, TEAM ENVI @-:ADVANMH:advIDE.Check=0|ENVI &PartCPYNoIDE=|EXIT _SUB
    LPOS &SPACOR=:,1,%&D1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DrvNum=%&SPACOR%,%&D1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DrvNum%, TEAM ENVI &IsIDE2=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE2%=3, TEAM ENVI @-:ADVANMH:advIDE.Check=0|ENVI &PartCPYNoIDE=|EXIT _SUB! TEAM ENVI @-:ADVANMH:advIDE.Check=1|ENVI &PartCPYNoIDE=-noide
_END

_SUB GIPICK
    ENVI @GITABL.Sel=?&&Sel
    ENVI @GITABL.Val=?%&Sel%.1;&GinCD
_END
_SUB OnTimer3
    ENVI @GIEDIT=正在搜索镜像文件，请稍候...  已用时间: %&K%秒
    CALC &K= %&K% + 0.2#1
_END

_SUB GIMsg1
    TEAM ENVI @Timer3=0| ENVI @GIEDIT.Visable=0
    FIND $%&GLSinISO%=,TEAM MESS 此ISO前三层目录内搜索不到符合条件的GHO镜像！|KILL \|EXIT _SUB
    ENVI @GITABL.Val=1*;%&GLSinISO%
_END

_SUB L_ISO2GHO
    CALL CheckUltraISODrv %&ISOPATH%
    TEAM ENVI &&ANYGHO=|ENVI &&aGHOLS=|ENVI &&HD45=|ENVI &&vln=|ENVI &&GTPATH= 
    FORX /S:2 %&FFDrv%:\*.GHO,&ANYGHO,0,ENVI &aGHOLS=%&aGHOLS%%&NLHH%%&ANYGHO%
    FORX *NL &aGHOLS,&vln,
    {
        FIND $%&vln%=,!
        {
            FNAM &HD45=%&vln%
            FIND $%&HD45%=HD4,! FIND $%&HD45%=HD5,! ENVI &GLSinISO=%&GLSinISO%%&vln%%&NLHH%
        }
    }
    ENVI @Timer3=0
    ENVI &KillVD=1
    ENVI @F_GHOinISO.POSTMSG=#1
_END

_SUB RESPATH
    BROW &&REPATH,,请选择镜像文件,GHO、WIM、SWM、ESD和ISO文件(*.GHO;*.WIM;*.SWM;*.ISO)|*.GHO;*.WIM;*.ESD;*.SWM;*.ISO,
    FIND $%&REPATH%=,!
    {
        FIND $%&REPATH%=%&PLIST1ITEM%,ENVI @GHOLIST.SEL=%&REPATH%!ENVI @GHOLIST.ADDSEL=%&REPATH%
        ENVI. @STATUS3=所选路径/文件：%GHOLIST%
        FEXT &&pEXT=%GHOLIST%
        FIND $%&pEXT%=GHO,! CALL WIMGICHECK "%GHOLIST%"
    }
_END

_SUB BACKPATH
    BROW &&BKPATH,&D:\SYSTEM.GHO,请选择保存目录,GHO、WIM和ESD文件(*.GHO;*.WIM;*.ESD)|*.GHO;*.WIM;*.ESD,
    FIND $%&BKPATH%=,!
    {
        // PECMD2012的BUG，通过【浏览】按钮添加文件时，当要添加的文件本来在下拉框就已存在
        // 且为第一个条目时，程序会退出。以下是为修正此BUG的。
        ENVI @GHOBACK.QUERY=&&AllBKGHO
        FIND $%&AllBKGHO%=,! ENVI @GHOBACK.QUERY=1;&&FirstBKGHO
        FIND $%&BKPATH%=%&FirstBKGHO%, ENVI @GHOBACK.SEL=%&BKPATH%! ENVI @GHOBACK.ADDSEL=%&BKPATH%
        ENVI. @STATUS3=所选路径/文件：%GHOBACK%
    }
_END

_SUB MAKEVIS1
    ENVI @RETIP=3.请选择镜像文件：
    ENVI @GHOBACK.Visable=0
    ENVI @BkBUTTON.Visable=0
    ENVI @GHOLIST.Visable=1
    ENVI @ReBUTTON.Visable=1
    ENVI @STATUS1=所选操作：还原分区
    ENVI. @STATUS3=所选路径/文件：%GHOLIST%
    ENVI @PLABE.Visable=1
    ENVI @DLABLE.Visable=0
    ENVI @SPART.Visable=0
    ENVI @DPART.Visable=0
    ENVI @STATUS2.Visable=1
    ENVI @STATUS4.Visable=0
    ENVI @STATUS3.Visable=1
    ENVI @STATUS5.Visable=0
    CALL SetNOIDE2
_END

_SUB MAKEVIS2
    ENVI @RETIP=3.请选择保存路径：
    ENVI @GHOLIST.Visable=0
    ENVI @ReBUTTON.Visable=0
    ENVI @GHOBACK.Visable=1
    ENVI @BkBUTTON.Visable=1
    ENVI @STATUS1=所选操作：备份分区
    ENVI. @STATUS3=所选路径/文件：%GHOBACK%
    ENVI @PLABE.Visable=1
    ENVI @DLABLE.Visable=0
    ENVI @SPART.Visable=0
    ENVI @DPART.Visable=0
    ENVI @STATUS2.Visable=1
    ENVI @STATUS4.Visable=0
    ENVI @STATUS3.Visable=1
    ENVI @STATUS5.Visable=0
    CALL SetNOIDE2
_END

_SUB MAKEVIS3
    ENVI @RETIP=2.请选择源分区：
    ENVI @GHOLIST.Visable=0
    ENVI @ReBUTTON.Visable=0
    ENVI @GHOBACK.Visable=0
    ENVI @BkBUTTON.Visable=0
    ENVI @PLABE.Visable=0
    ENVI @DLABLE.Visable=1
    ENVI @SPART.Visable=1
    ENVI @DPART.Visable=1
    ENVI @STATUS1=所选操作：分区对拷
    ENVI @STATUS2.Visable=0
    ENVI @STATUS4.Visable=1
    ENVI @STATUS4=源分区：      %SPART%
    ENVI @STATUS3.Visable=0
    ENVI @STATUS5.Visable=1
    ENVI @STATUS5=目标分区：    %DPART%
    CALL PARTCOPYNOIDE
_END

_SUB REORBK
    FIND $%RERADI.Check%=0,!!FIND $%BKRADI.Check%=0,!!FIND $%PART2PART.Check%=0,!!TEAM MESS 您还没有选择操作！%&NLDD%%&NLDD%请选择【还原分区】、【备份分区】或【分区对拷】！|EXIT _SUB
    FIND $%PART2PART.Check%=0,!!
    {
        FIND $%&PARTSEL1%=,!!FIND $%&PARTSEL2%=,!!TEAM MESS 您还没有选择分区！%&NLDD%%&NLDD%请选择分区！|EXIT _SUB
        FIND $%RERADI.Check%=1,
        {
            RSTR &&REL4=4,%STATUS3%
            FIND $%&REL4%=.GHO, TEAM CALL REGHOST|EXIT _SUB
            LPOS* &&WIMFlag=->,1,%STATUS3%
            IFEX $%&WIMFlag% > 0, TEAM CALL RESTOREWIM|EXIT _SUB
            FIND $%&REL4%=.ISO, TEAM MESS. 您当前选的是%GHOLIST%文件，%&NLDD%%&NLDD%请再选一下此ISO文件，看看有没有您需要的镜像！|EXIT _SUB
            FIND $%&REL4%=.WIM, TEAM MESS. 您当前选的是%GHOLIST%文件，%&NLDD%%&NLDD%请再选一下此WIM文件，看看有没有您需要的卷！|EXIT _SUB
            FIND $%&REL4%=.ESD, TEAM MESS. 您当前选的是%GHOLIST%文件，%&NLDD%%&NLDD%请再选一下此ESD文件，看看有没有您需要的卷！|EXIT _SUB
            FIND $%&REL4%=.SWM, TEAM MESS. 您当前选的是%GHOLIST%文件，%&NLDD%%&NLDD%请再选一下此SWM文件，看看有没有您需要的卷！|EXIT _SUB
            TEAM MESS 您还没有选择镜像！|EXIT _SUB
        }
        FIND $%BKRADI.Check%=1,
        {
            MSTR &&BKBLANK=<1>%GHOBACK%
            FIND $%&BKBLANK%=,TEAM MESS 您还没有选择保存路径！|EXIT _SUB
            RSTR &&BKEXT=4,%GHOBACK%
            FIND $%&BKEXT%=.WIM, TEAM CALL BACKUPWIM|EXIT _SUB
            FIND $%&BKEXT%=.ESD, TEAM CALL BACKUPWIM|EXIT _SUB
            CALL BKGHOST
        }
    }
    FIND $%PART2PART.Check%=1,!!
    {
        FIND $%SPART%=,TEAM MESS 您还没有选择源分区！|EXIT _SUB
        FIND $%DPART%=,TEAM MESS 您还没有选择目标分区！|EXIT _SUB
        CALL P2PDUMP
    }
_END

_SUB REGHOST
    LPOS &&pPOS=：,1,%STATUS3%
    CALC #&pPOS = %&pPOS% + 1
    MSTR &&pFILE=%&pPOS%,0,%STATUS3%
    FDRV &&pDrv=%&pFILE%
    FIND $%&pDrv%=%&PARTSEL2%,TEAM MESS GHO镜像所在分区与目标分区相同，无法还原！%&NLDD%%&NLDD%可将此GHO镜像复制到其它分区再进行还原。|EXIT _SUB
    FEXT &&pEXT=%GHOLIST%
    FIND $%&pEXT%=ISO,
    {
        FDRV &&pDrv2=%GHOLIST%
        FIND $%&pDrv2%=%&PARTSEL2%,TEAM MESS ISO文件所在分区与目标分区相同，无法还原！%&NLDD%%&NLDD%可将此ISO文件复制到其它分区再进行还原。|EXIT _SUB        
    }
    TEAM ENVI &&szNoIDE=| ENVI &&pCRC=| ENVI &&PWDRE=|ENVI &&szNoUSB=
    CALL CRPWD "%&pFILE%"
    FDRV &&szDrv=%GHOLIST%
    CALL GetNoIDENoUSB %pBusType% %&szDrv%
    FIND $%advCRC.Check%=1, ENVI &pCRC=-crcignore
    IFEX %&pFILE%, TEAM CALL OnRestore|EXIT _SUB
    MESS 找不到所选GHO镜像！
_END

_SUB GetNoIDENoUSB
    TEAM ENVI &&szTYPE=|ENVI &&szBUS=0|ENVI &&nBUS=|ENVI &&Drv=
    ENVI &nBUS=%1
    ENVI &Drv=%2
    FORM &szTYPE,&szBUS=%&Drv%
    IFEX $%&nBUS% = 3,! IFEX $%&szBUS% = 3,! ENVI &szNoIDE=-noide
    IFEX $%&nBUS% = 7,! IFEX $%&szBUS% = 7,! ENVI &szNoUSB=-nousb
_END

_SUB ASKGHORestore,W432H172,还原分区,,#1,
    ENVI &&dstPart=
    FIND $%&PARTSEL2%=  , ENVI &dstPart=%&PARTSEL1% 分区! ENVI &dstPart=%&PARTSEL2%
    LABE. -left ,L26T16W400H31,把"%&pFILE%"还原到 %&dstPart%,,0xFF0000
    LABE ,L26T56W61H18,完成后：,,
    CHEK GHORestoreSHUT,L230T53W62H18,关机,CALL GHOReSHUTRB1,0
    CHEK GHORestoreRB,L295T53W62H18,重启,CALL GHOReSHUTRB2,0
    ITEM ,L226T98W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L326T98W80H28,取 消,KILL \,
_END

_SUB GHOReSHUTRB1
    FIND $%GHORestoreSHUT.Check%=1, ENVI @GHORestoreRB.Check=0
_END

_SUB GHOReSHUTRB2
    FIND $%GHORestoreRB.Check%=1, ENVI @GHORestoreSHUT.Check=0
_END

_SUB OnRestore
    IFEX $%&PEPOS% = 0,!! FIND $%&PARTSEL2%=%SYSTEMDRIVE%,!! TEAM MESS 请到PE中还原系统|EXIT _SUB
    ENVI &&IsConfirm=0
    CALL ASKGHORestore
    FIND $%&IsConfirm%=0, EXIT _SUB
    TEAM ENVI &&TDrvNum=|ENVI &&Tstyle=|ENVI &&EFIDrive=|ENVI &&ActiveDrv=
    CALL GetTargetPartitionInfo
    // 动态磁盘
    FIND $%&PARTSEL5%=Dynamic, CALL GetNumberOfVolume
    ENVI @MHGHO2012.Visable=0
    ENVI &&RUNINFO1=0
    EXEC* -exe:*#200 &RUNINFO1=!ghost.exe -clone,mode=pload,src="%&pFILE%":1,dst=%&PARTSEL1% -batch %&szNoIDE% %&szNoUSB% %&pCRC% %&PWDRE% %paras%
    FIND $%&RUNINFO1%=,
    { 
        MESS+icon102 还原成功！@还原分区 #OK *3000 $1
        CALL AutomaticGuidanceRepair      
        FIND $%GHORestoreSHUT.Check%=1, ENVI &SHUTorREBOOT=1
        FIND $%GHORestoreRB.Check%=1, ENVI &SHUTorREBOOT=2
        ENVI @MHGHO2012.Visable=1
        KILL @MHGHO2012
        EXIT _SUB
    }
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    FILE ghstwarn.txt
    ENVI &&ERRPOS=0
    LPOS* &ERRPOS=T: 36002,1,%&RUNINFO1%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 用户终止，还原失败！@还原分区 #OK *5000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    
    FIND $%&PARTSEL5%=Dynamic,!!
    {
        ENVI &&RUNINFO2=0
        EXEC* -exe:*#200 &RUNINFO2=!ghost.EXE -clone,mode=pload,src="%&pFILE%":1,dst=@OS:%&DrvLettBackup% -batch %&szNoIDE% %&szNoUSB% %&pCRC% %&PWDRE% %paras%
        FIND $%&RUNINFO2%=,
        {
            MESS+icon102 还原成功！@还原分区 #OK *3000 $1
            FIND $%GHORestoreSHUT.Check%=1, ENVI &SHUTorREBOOT=1
            FIND $%GHORestoreRB.Check%=1, ENVI &SHUTorREBOOT=2
            ENVI @MHGHO2012.Visable=1
            KILL @MHGHO2012
            EXIT _SUB
        }
        FILE ghost*.dmp
        FILE GHOSTERR.TXT
        LPOS* &ERRPOS=T: 36002,1,%&RUNINFO2%
        IFEX $%&ERRPOS% > 0,!!
        {
            MESS 用户终止，还原失败！@还原分区 #OK *5000 $1
            ENVI @MHGHO2012.Visable=1
            EXIT _SUB
        }
    }
    // 分区偏移值有问题的话 ---开始还原-----
    FIND $%&DrvLettBackup%=,! FIND $%&PARTSEL5%=Dynamic,!
    {
        ENVI &&RUNINFO2=0
        EXEC* -exe:*#200 &RUNINFO2=!ghost.EXE -clone,mode=pload,src="%&pFILE%":1,dst=@OS:%&DrvLettBackup% -batch %&szNoIDE% %&szNoUSB% %&pCRC% %&PWDRE% %paras%
        FIND $%&RUNINFO2%=,
        {
            MESS+icon102 还原成功！@还原分区 #OK *3000 $1
            FIND $%GHORestoreSHUT.Check%=1, ENVI &SHUTorREBOOT=1
            FIND $%GHORestoreRB.Check%=1, ENVI &SHUTorREBOOT=2
            ENVI @MHGHO2012.Visable=1
            KILL @MHGHO2012
            EXIT _SUB
        }
        FILE ghost*.dmp
        FILE GHOSTERR.TXT
        LPOS* &ERRPOS=T: 36002,1,%&RUNINFO2%
        IFEX $%&ERRPOS% > 0,!!
        {
            MESS 用户终止，还原失败！@还原分区 #OK *5000 $1
            ENVI @MHGHO2012.Visable=1
            EXIT _SUB
        }
    }
    // 分区偏移值有问题的话 ---结束还原-----
    MESS 还原失败！@还原分区 #OK *3000 $1
    ENVI @MHGHO2012.Visable=1
_END

_SUB ASKGHOBackup,W432H172,备份分区,,#1,,
    ENVI &&dstPart=
    FIND $%&PARTSEL2%=  , ENVI &dstPart=%&PARTSEL1% 分区! ENVI &dstPart=%&PARTSEL2%
    LABE. -left ,L26T16W400H31,把 %&dstPart% 备份到"%&BGHOPATH%",,0xFF0000
    LABE ,L26T56W61H18,完成后：,,
    CHEK GHOBackupSHUT,L88T53W62H18,关机,CALL GHOBkSHUTRB1,0
    CHEK GHOBackupRB,L152T53W62H18,重启,CALL GHOBkSHUTRB2,0
    ITEM ,L226T98W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L326T98W80H28,取 消,KILL \,
_END

_SUB GHOBkSHUTRB1
    FIND $%GHOBackupSHUT.Check%=1, ENVI @GHOBackupRB.Check=0
_END

_SUB GHOBkSHUTRB2
    FIND $%GHOBackupRB.Check%=1, ENVI @GHOBackupSHUT.Check=0
_END

_SUB ASKExistGHOBackup,W432H200,备份分区,,#1,,
    ENVI &&dstPart=
    FIND $%&PARTSEL2%=  , ENVI &dstPart=%&PARTSEL1% 分区! ENVI &dstPart=%&PARTSEL2%
    LABE. -left ,L26T16W400H31,把 %&dstPart% 备份到"%&BGHOPATH%",,0xFF0000
    LABE. -left ,L26T54W360H18,将覆盖原有的备份文件！,,0x0000FF
    LABE ,L26T86W61H18,完成后：,,
    CHEK ExistGHOBackupSHUT,L88T83W62H18,关机,CALL ExistGHOBkSHUTRB1,0
    CHEK ExistGHOBackupRB,L152T83W62H18,重启,CALL ExistGHOBkSHUTRB2,0
    ITEM ,L230T120W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L330T120W80H28,取 消,KILL \,
_END

_SUB ExistGHOBkSHUTRB1
    FIND $%ExistGHOBackupSHUT.Check%=1, ENVI @ExistGHOBackupRB.Check=0
_END

_SUB ExistGHOBkSHUTRB2
    FIND $%ExistGHOBackupRB.Check%=1, ENVI @ExistGHOBackupSHUT.Check=0
_END

_SUB CheckBKPathLegal
    ENVI &&DrvORNum=%~1
    STRL &iLen=%&DrvORNum%
    IFEX $%&iLen% > 2, TEAM CALL CheckLegalByNum "%&DrvORNum%"|EXIT _SUB
    IFEX $%&iLen% = 2, TEAM ENVI &RealBKDrvLett=%&DrvORNum%|CALL CheckLegalByDrv "%&DrvORNum%"
_END

_SUB CheckLegalByNum
    ENVI &&szDrvPartNum=%~1
    TEAM ENVI &&RChar1=|ENVI &&DrvPartNum=|ENVI &&vLn=|ENVI &&A1=|ENVI &&A2=
    RSTR &RChar1=1,%&szDrvPartNum%
    FIND $%&RChar1%=:,MSTR &DrvPartNum=-2,0,%&szDrvPartNum%! ENVI &DrvPartNum=%&szDrvPartNum%
    FORX *NL &vFORM,&vLn,
    {
        MSTR* &A1,&A2=<1><2>%&vLn%
        FIND $%&A1%=%&DrvPartNum%, TEAM ENVI &legalDrv=%&A2%|EXIT FORX
    }
    FIND $%&legalDrv%=,! FIND $%&legalDrv%=  ,! ENVI &RealBKDrvLett=%&legalDrv%
_END

_SUB CheckLegalByDrv
    ENVI &&Drv=%~1
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A2=
    FORX *NL &vFORM,&vLn,
    {
        MSTR* &A1,&A2=<1><2>%&vLn%
        FIND $%&A2%=%&Drv%,TEAM ENVI &legalNum=%&A1%|EXIT FORX
    }
_END

_SUB BKGHOST
    TEAM ENVI &&pBLK=|ENVI &&szDrive=|ENVI &&szDrvPOS=0|ENVI &&szBKPATH=
    MSTR &pBLK=<1->%GHOBACK%
    LPOS &szDrvPOS=\,1,%&pBLK%
    IFEX $%&szDrvPOS% = 0, TEAM MESS 请选择合法的保存路径。|EXIT _SUB
    MSTR &szBKPATH=%&szDrvPOS%,0,%&pBLK%
    CALC #&szDrvPOS = %&szDrvPOS% - 1
    LSTR &szDrive=%&szDrvPOS%,%&pBLK%
    TEAM ENVI &&legalDrv=|ENVI &&legalNum=|ENVI &&RealBKDrvLett=
    CALL CheckBKPathLegal "%&szDrive%"
    FIND $%&legalDrv%=,!! FIND $%&legalNum%=,!! TEAM MESS 备份的保存路径不合法，请重新指定。|EXIT _SUB
    FIND $%&RealBKDrvLett%=%&PARTSEL2%, TEAM MESS 无法把备份文件保存到要备份的分区！%&NLDD%%&NLDD%请重新选择保存路径！|EXIT _SUB
    // 如果备份到光驱中则提示
    FIND $%&RealBKDrvLett%=,!
    {
        TEAM ENVI &&szBKTYPE=|ENVI &&dwBKBUS=0
        FORM &szBKTYPE,&dwBKBUS=%&RealBKDrvLett%
        FIND $DRIVE_CDROM=%&szBKTYPE%, TEAM MESS 无法备份到光驱%&RealBKDrvLett%中，请重新指定备份路径。|EXIT _SUB
    }
    RSTR &&BKL4=4,%&pBLK%
    FIND $%&RealBKDrvLett%=,
    {
        FIND $%&BKL4%=.GHO, ENVI &BGHOPATH=%&pBLK%! ENVI &BGHOPATH=%&pBLK%.GHO
    }
    FIND $%&RealBKDrvLett%=,!
    {
        FIND $%&BKL4%=.GHO, ENVI &BGHOPATH=%&RealBKDrvLett%%&szBKPATH%! ENVI &BGHOPATH=%&RealBKDrvLett%%&szBKPATH%.GHO
    }
    RPOS &&pDIR=\,1,%&BGHOPATH%
    LSTR &&pMKDIR=%&pDIR%,%&BGHOPATH%
    ENVI &&ExistFolder=0
    IFEX %&pMKDIR%, ENVI &ExistFolder=1!MDIR %&pMKDIR%
    FIND $%HideFolder.Check%=1, IFEX %&pMKDIR%, SITE %&pMKDIR%,+H
    MSTR &&pSIZE=<1>%advBL02%
    TEAM ENVI &&szNoIDE=|ENVI &&szNoUSB=| ENVI &&BKPWD=| ENVI &&pCMPR=-z1| ENVI &&pSPLIT=-split=%&pSIZE%
    FIND $%advPWD1.Check%=1,
    {
        FIND $%advEDIT1%=,!
        {
            TEAM ENVI &&realPWD=|ENVI &&PL=
            ENVI &realPWD=%advEDIT1%
            STRL &PL=%&realPWD%
            IFEX $%&PL% > 10, LSTR &realPWD=10,%&realPWD%
            ENVI &BKPWD=-pwd="%&realPWD%"
        }
    }
    CALL GetNoIDENoUSB %pBusType% %&szDrive%
    FIND $%advBL01%=不压缩, ENVI &pCMPR=
    FIND $%advBL01%=高压缩, ENVI &pCMPR=-z3
    FIND $%advBL01%=极限压缩, ENVI &pCMPR=-z9
    FIND $%advBL02%=不分卷, ENVI &pSPLIT=-split=0
    FIND $%advBL02%=自动检测, ENVI &pSPLIT=
    TEAM ENVI &&IsConfirm=0|ENVI &&dstFileExist=0
    IFEX %&BGHOPATH%, TEAM ENVI &dstFileExist=1|CALL ASKExistGHOBackup! CALL ASKGHOBackup
    FIND $%&IsConfirm%=0,
    {
        IFEX $%&ExistFolder% = 0,!!
        {
            MSTR &&KillDir=-2,0,%&pMKDIR%
            SITE %&KillDir%,-H-S-R
            PATH #%&KillDir%
        }
        EXIT _SUB
    }
    TEAM ENVI &&CurrentSystem=0|ENVI &&BackupSuccess=0
    TEAM ENVI &&iTIME=|ENVI &&NewGHOTime=0|ENVI &&NewGHOSize=0
    TEAM ENVI &&T1=|ENVI &&T2=|ENVI &&T3=|ENVI &&T4=|ENVI &&T5=|ENVI &&T6=|ENVI &&T7=
    IFEX $%&PEPOS% = 0,!! FIND $%&PARTSEL2%=%SYSTEMDRIVE%,!! ENVI &CurrentSystem=1
    ENVI &OldGHOExist=0
    IFEX %&BGHOPATH%,
    {
        ENVI &OldGHOExist=1
        SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &OldGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    FIND $%&PARTSEL5%=Dynamic, CALL GetNumberOfVolume
    IFEX $%&CurrentSystem% = 1,!!
    {
        PUTF %SystemRoot%\bootstat.dat,0x08#0x02,0x00 0x00
        FIND $%&RealBKDrvLett%=,! TEAM ENVI &I=0|ENVI @&KillGHOTimer=2000
    }
    ENVI @MHGHO2012.Visable=0
    TEAM ENVI &&RUNINFO1=0|ENVI &&report=0|ENVI &KillGHOFlag=0
    EXEC* -exe:*#200 &RUNINFO1=!ghost.EXE -clone,mode=pdump,src=%&PARTSEL1%,dst="%&BGHOPATH%" -batch %&szNoIDE% %&szNoUSB% %&BKPWD% %&pCMPR% %&pSPLIT% %paras%
    ENVI @&KillGHOTimer=0
    IFEX %&BGHOPATH%,
    {
        SIZE &NewGHOSize=%&BGHOPATH%
        SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &NewGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    IFEX $%&KillGHOFlag% = 1,!!
    {
        FIND $%&PARTSEL5%=Dynamic,!
        {
            MESS 无法热备份当前系统，请在PE中备份。@备份分区 #OK *5000 $1
            FILE ghost*.dmp
            FILE GHOSTERR.TXT
            FILE ghstwarn.txt
            FIND $%&NewGHOTime%=%&OldGHOTime%,! FILE %&BGHOPATH%
            IFEX $%&ExistFolder% = 0,!!
            {
                MSTR &&KillDir=-2,0,%&pMKDIR%
                SITE %&KillDir%,-H-S-R
                PATH #%&KillDir%
            }
            ENVI @MHGHO2012.Visable=1            
            EXIT _SUB
        }
    }
    IFEX $%&KillGHOFlag% = 0,
    {
    FIND $%&RUNINFO1%=,
    {
        IFEX %&BGHOPATH%,
        {
            IFEX $%&OldGHOExist% = 1,!!
            {
                FIND $%&NewGHOTime%=%&OldGHOTime%,!!
                {
                    FIND $%&PARTSEL5%=Dynamic,! TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                }
                FIND $%&NewGHOTime%=%&OldGHOTime%,!
                {
                    IFEX $%&CurrentSystem% = 1, CALL CheckBackupSuccess %&NewGHOSize%
                    IFEX $%&CurrentSystem% = 0,!!
                    {
                        IFEX $%&NewGHOSize% = 0,!
                        {
                            MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                            IFEX $%&dstFileExist% = 0,!!
                            {
                                FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                            }
                            IFEX $%&dstFileExist% = 1,!!
                            {
                                FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                            }
                            ENVI @MHGHO2012.Visable=1
                            KILL @MHGHO2012
                            EXIT _SUB
                        }
                        IFEX $%&NewGHOSize% = 0,!! FIND $%&PARTSEL5%=Dynamic,! TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                    }
                }
            }
            IFEX $%&OldGHOExist% = 0,!!
            {
                IFEX $%&CurrentSystem% = 1, CALL CheckBackupSuccess %&NewGHOSize%
                IFEX $%&CurrentSystem% = 0,!!
                {
                    IFEX $%&NewGHOSize% = 0,!
                    {
                        MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                        IFEX $%&dstFileExist% = 0,!!
                        {
                            FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                            FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                        }
                        IFEX $%&dstFileExist% = 1,!!
                        {
                            FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                            FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                        }
                        ENVI @MHGHO2012.Visable=1
                        KILL @MHGHO2012
                        EXIT _SUB
                    }
                    IFEX $%&NewGHOSize% = 0,!! FIND $%&PARTSEL5%=Dynamic,! TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                }
            }
            IFEX $%&BackupSuccess% = 1,!!
            {
                MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                IFEX $%&dstFileExist% = 0,!!
                {
                    FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                    FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                }
                IFEX $%&dstFileExist% = 1,!!
                {
                    FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                    FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                }
                ENVI @MHGHO2012.Visable=1
                KILL @MHGHO2012
                EXIT _SUB
            }
        }
        IFEX %&BGHOPATH%,!
        {
            FIND $%&PARTSEL5%=Dynamic,!
            {
                TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
            }
        }
    }
    }
    // 以上最后一个花括号对应&KillGHOFlag
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    FILE ghstwarn.txt
    FIND $%&NewGHOTime%=%&OldGHOTime%,! FILE %&BGHOPATH%
    IFEX $%&ExistFolder% = 0,!!
    {
        MSTR &&KillDir=-2,0,%&pMKDIR%
        SITE %&KillDir%,-H-S-R
        PATH #%&KillDir%
    }
    ENVI &&ERRPOS=0
    LPOS* &ERRPOS=T: 651,1,%&RUNINFO1%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 保存镜像的分区空间不足，备份失败！@备份分区 #OK *10000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    LPOS* &ERRPOS=T: 519,1,%&RUNINFO1%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 保存镜像的分区空间不足，备份失败！@备份分区 #OK *10000 $1
        ENVI @MHGHO2012.Visable=1        
        EXIT _SUB
    }
    LPOS* &ERRPOS=T: 36002,1,%&RUNINFO1%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 用户终止，备份失败！@备份分区 #OK *5000 $1
        ENVI @MHGHO2012.Visable=1        
        EXIT _SUB
    }  
    FIND $%&PARTSEL5%=Dynamic,!!
    {
        ENVI &ExistFolder=0
        IFEX %&pMKDIR%, ENVI &ExistFolder=1!MDIR %&pMKDIR%
        FIND $%HideFolder.Check%=1, IFEX %&pMKDIR%, SITE %&pMKDIR%,+H
        ENVI &OldGHOExist=0
        IFEX %&BGHOPATH%,
        {
            ENVI &OldGHOExist=1
            SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
            MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
            ENVI &OldGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
        }
        ENVI &&RUNINFO2=0
        ENVI &report=0
        EXEC* -exe:*#200 &RUNINFO2=!ghost.EXE -clone,mode=pdump,src=@OS:%&DrvLettBackup%,dst="%&BGHOPATH%" -batch %&szNoIDE% %&szNoUSB% %&BKPWD% %&pCMPR% %&pSPLIT% %paras%
       
        IFEX %&BGHOPATH%,
        {
            SIZE &NewGHOSize=%&BGHOPATH%
            SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
            MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
            ENVI &NewGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
        }
        FIND $%&RUNINFO2%=,
        {
            IFEX %&BGHOPATH%,!!
            {
                IFEX $%&OldGHOExist% = 1,!!
                {
                    FIND $%&NewGHOTime%=%&OldGHOTime%,!!
                    {
                        TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                    }
                    FIND $%&NewGHOTime%=%&OldGHOTime%,!
                    {
                        IFEX $%&CurrentSystem% = 1, CALL CheckBackupSuccess %&NewGHOSize%
                        IFEX $%&CurrentSystem% = 0,!!
                        {
                            IFEX $%&NewGHOSize% = 0,!
                            {
                                MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                                IFEX $%&dstFileExist% = 0,!!
                                {
                                    FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                    FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                                }
                                IFEX $%&dstFileExist% = 1,!!
                                {
                                    FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                    FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                                }
                                ENVI @MHGHO2012.Visable=1
                                KILL @MHGHO2012
                                EXIT _SUB
                            }
                            IFEX $%&NewGHOSize% = 0, TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                        }
                    }
                }
                IFEX $%&OldGHOExist% = 0,!!
                {
                    IFEX $%&CurrentSystem% = 1, CALL CheckBackupSuccess %&NewGHOSize%
                    IFEX $%&CurrentSystem% = 0,!!
                    {
                        IFEX $%&NewGHOSize% = 0,!
                        {
                            MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                            IFEX $%&dstFileExist% = 0,!!
                            {
                                FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                            }
                            IFEX $%&dstFileExist% = 1,!!
                            {
                                FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                            }
                            ENVI @MHGHO2012.Visable=1
                            KILL @MHGHO2012
                            EXIT _SUB
                        }
                        IFEX $%&NewGHOSize% = 0, TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                    }
                }
                IFEX $%&BackupSuccess% = 1,!!
                {
                    MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                    IFEX $%&dstFileExist% = 0,!!
                    {
                        FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                        FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                    }
                    IFEX $%&dstFileExist% = 1,!!
                    {
                        FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                        FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                    }
                    ENVI @MHGHO2012.Visable=1
                    KILL @MHGHO2012
                    EXIT _SUB
                }
            }
            IFEX %&BGHOPATH%,! TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
       }
       FILE ghost*.dmp
       FILE GHOSTERR.TXT
       FIND $%&NewGHOTime%=%&OldGHOTime%,! FILE %&BGHOPATH%
       IFEX $%&ExistFolder% = 0,!!
       {
           MSTR &&KillDir=-2,0,%&pMKDIR%
           SITE %&KillDir%,-H-S-R
           PATH #%&KillDir%
       }
       LPOS* &ERRPOS=T: 651,1,%&RUNINFO2%
       IFEX $%&ERRPOS% > 0,!!
       {
           MESS 保存镜像的分区空间不足，备份失败！@备份分区 #OK *10000 $1
           ENVI @MHGHO2012.Visable=1
           EXIT _SUB
       }
       LPOS* &ERRPOS=T: 519,1,%&RUNINFO2%
       IFEX $%&ERRPOS% > 0,!!
       {
           MESS 保存镜像的分区空间不足，备份失败！@备份分区 #OK *10000 $1
           ENVI @MHGHO2012.Visable=1
           EXIT _SUB
       }
       LPOS* &ERRPOS=T: 36002,1,%&RUNINFO2%
       IFEX $%&ERRPOS% > 0,!!
       {
           MESS 用户终止，备份失败！@备份分区 #OK *5000 $1
           ENVI @MHGHO2012.Visable=1         
           EXIT _SUB
       }
    }
    // 分区偏移值有问题的话 ---开始-----
    FIND $%&DrvLettBackup%=,! FIND $%&PARTSEL5%=Dynamic,!
    {
        ENVI &ExistFolder=0
        IFEX %&pMKDIR%, ENVI &ExistFolder=1!MDIR %&pMKDIR%
        FIND $%HideFolder.Check%=1, IFEX %&pMKDIR%, SITE %&pMKDIR%,+H
        ENVI &OldGHOExist=0
        IFEX %&BGHOPATH%,
        {
            ENVI &OldGHOExist=1
            SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
            MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
            ENVI &OldGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
        }
        ENVI &&RUNINFO2=0
        ENVI &report=0
        EXEC* -exe:*#200 &RUNINFO2=!ghost.EXE -clone,mode=pdump,src=@OS:%&DrvLettBackup%,dst="%&BGHOPATH%" -batch %&szNoIDE% %&szNoUSB% %&BKPWD% %&pCMPR% %&pSPLIT% %paras%
       
        IFEX %&BGHOPATH%,
        {
            SIZE &NewGHOSize=%&BGHOPATH%
            SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
            MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
            ENVI &NewGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
        }
        FIND $%&RUNINFO2%=,
        {
            IFEX %&BGHOPATH%,!!
            {
                IFEX $%&OldGHOExist% = 1,!!
                {
                    FIND $%&NewGHOTime%=%&OldGHOTime%,!!
                    {
                        TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                    }
                    FIND $%&NewGHOTime%=%&OldGHOTime%,!
                    {
                        IFEX $%&CurrentSystem% = 1, CALL CheckBackupSuccess %&NewGHOSize%
                        IFEX $%&CurrentSystem% = 0,!!
                        {
                            IFEX $%&NewGHOSize% = 0,!
                            {
                                MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                                IFEX $%&dstFileExist% = 0,!!
                                {
                                    FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                    FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                                }
                                IFEX $%&dstFileExist% = 1,!!
                                {
                                    FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                    FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                                }
                                ENVI @MHGHO2012.Visable=1
                                KILL @MHGHO2012
                                EXIT _SUB
                            }
                            IFEX $%&NewGHOSize% = 0, TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                        }
                    }
                }
                IFEX $%&OldGHOExist% = 0,!!
                {
                    IFEX $%&CurrentSystem% = 1, CALL CheckBackupSuccess %&NewGHOSize%
                    IFEX $%&CurrentSystem% = 0,!!
                    {
                        IFEX $%&NewGHOSize% = 0,!
                        {
                            MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                            IFEX $%&dstFileExist% = 0,!!
                            {
                                FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                            }
                            IFEX $%&dstFileExist% = 1,!!
                            {
                                FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                                FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                            }
                            ENVI @MHGHO2012.Visable=1
                            KILL @MHGHO2012
                            EXIT _SUB
                        }
                        IFEX $%&NewGHOSize% = 0, TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
                    }
                }
                IFEX $%&BackupSuccess% = 1,!!
                {
                    MESS+icon102 备份成功！@备份分区 #OK *3000 $1
                    IFEX $%&dstFileExist% = 0,!!
                    {
                        FIND $%GHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                        FIND $%GHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                    }
                    IFEX $%&dstFileExist% = 1,!!
                    {
                        FIND $%ExistGHOBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                        FIND $%ExistGHOBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                    }
                    ENVI @MHGHO2012.Visable=1
                    KILL @MHGHO2012
                    EXIT _SUB
                }
            }
            IFEX %&BGHOPATH%,! TEAM ENVI &report=1|MESS 备份失败！ @备份分区 #OK *3000 $1
       }
       FILE ghost*.dmp
       FILE GHOSTERR.TXT
       FIND $%&NewGHOTime%=%&OldGHOTime%,! FILE %&BGHOPATH%
       IFEX $%&ExistFolder% = 0,!!
       {
           MSTR &&KillDir=-2,0,%&pMKDIR%
           SITE %&KillDir%,-H-S-R
           PATH #%&KillDir%
       }
       LPOS* &ERRPOS=T: 651,1,%&RUNINFO2%
       IFEX $%&ERRPOS% > 0,!!
       {
           MESS 保存镜像的分区空间不足，备份失败！@备份分区 #OK *10000 $1
           ENVI @MHGHO2012.Visable=1        
           EXIT _SUB
       }
       LPOS* &ERRPOS=T: 519,1,%&RUNINFO2%
       IFEX $%&ERRPOS% > 0,!!
       {
           MESS 保存镜像的分区空间不足，备份失败！@备份分区 #OK *10000 $1
           ENVI @MHGHO2012.Visable=1           
           EXIT _SUB
       }
       LPOS* &ERRPOS=T: 36002,1,%&RUNINFO2%
       IFEX $%&ERRPOS% > 0,!!
       {
           MESS 用户终止，备份失败！@备份分区 #OK *5000 $1
           ENVI @MHGHO2012.Visable=1
           EXIT _SUB
       }
    }
    // 分区偏移值有问题的话 ---结束-----
    IFEX $%&report% = 0, MESS 备份失败！@备份分区 #OK *3000 $1
    ENVI @MHGHO2012.Visable=1
_END

_SUB CheckBackupSuccess
    ENVI &&GHOSize=%1
    FIND $%&VERNUM%=5.1,!!
    {
        IFEX $%&GHOSize% >= 100M, ENVI &BackupSuccess=1
        EXIT _SUB
    }
    FIND $%&VERNUM%=5.2,!!
    {
        IFEX $%&GHOSize% >= 100M, ENVI &BackupSuccess=1
        EXIT _SUB
    }
    FIND $%&VERNUM%=6.0,!!
    {
        IFEX $%&GHOSize% >= 280M, ENVI &BackupSuccess=1
        EXIT _SUB
    }
    FIND $%&VERNUM%=6.1,!!
    {
        IFEX $%&GHOSize% >= 300M, ENVI &BackupSuccess=1
        EXIT _SUB
    }
    IFEX $%&VERNUM% > 6.1,!!
    {
        IFEX $%&GHOSize% >= 450M, ENVI &BackupSuccess=1
        EXIT _SUB
    }
    IFEX $%&VERNUM% < 5.1,!!
    {
        IFEX $%&GHOSize% >= 80M, ENVI &BackupSuccess=1
        EXIT _SUB
    }
_END

_SUB OnKillGHOTimer
    CALC #&I = %&I% + 2
    TEAM ENVI &&iTIME=|ENVI &&T1=|ENVI &&T2=|ENVI &&T3=|ENVI &&T4=|ENVI &&T5=|ENVI &&T6=|ENVI &&T7=
    IFEX %&BGHOPATH%,
    {
        SIZE &CheckGHOSize=%&BGHOPATH%
        SITE ?-local ,&iTIME=FTIME,%&BGHOPATH%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &CheckGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    IFEX $%&I% < 40,!!
    {
        IFEX $%&OldGHOExist% = 0,!! IFEX %&BGHOPATH%,!! IFEX $%&CheckGHOSize% = 0,! TEAM ENVI @&KillGHOTimer=0|EXIT _SUB
        IFEX $%&OldGHOExist% = 1,!! FIND $%&CheckGHOTime%=%&OldGHOTime%,! IFEX $%&CheckGHOSize% = 0,! TEAM ENVI @&KillGHOTimer=0|EXIT _SUB
    }
    IFEX $%&I% >= 40,!!
    {
        ENVI @&KillGHOTimer=0
        IFEX %&BGHOPATH%,!
        {
            ENVI &KillGHOFlag=1
            KILL *force ghost.EXE
            FILE ghost*.dmp
            FILE GHOSTERR.TXT
            FILE ghstwarn.txt
            EXIT _SUB
        }
        IFEX %&BGHOPATH%,!!
        {
            IFEX $%&OldGHOExist% = 0,
            {
                IFEX $%&CheckGHOSize% = 0,! EXIT _SUB
                IFEX $%&CheckGHOSize% = 0,!!
                {
                    ENVI &KillGHOFlag=1
                    KILL *force ghost.EXE
                    FILE ghost*.dmp
                    FILE GHOSTERR.TXT
                    FILE ghstwarn.txt
                    EXIT _SUB
                }
            }
            IFEX $%&OldGHOExist% = 1,
            {
                FIND $%&CheckGHOTime%=%&OldGHOTime%,!!
                {
                    ENVI &KillGHOFlag=1
                    KILL *force ghost.EXE
                    FILE ghost*.dmp
                    FILE GHOSTERR.TXT
                    FILE ghstwarn.txt
                    EXIT _SUB
                }
                FIND $%&CheckGHOTime%=%&OldGHOTime%,!
                {
                    IFEX $%&CheckGHOSize% = 0,! EXIT _SUB
                    IFEX $%&CheckGHOSize% = 0,!!
                    {
                        ENVI &KillGHOFlag=1
                        KILL *force ghost.EXE
                        FILE ghost*.dmp
                        FILE GHOSTERR.TXT
                        FILE ghstwarn.txt
                        EXIT _SUB
                    }
                }
            }
        }
    }
_END

_SUB ASKPartitionClone,W320H202,分区对拷,,#1,,
    TEAM ENVI &&srcDRVforWIN=|ENVI &&dstDRVforWIN=
    FIND $%&SRSLett%=, ENVI &srcDRVforWIN=%&SRCNUM%! ENVI &srcDRVforWIN=%&SRSLett%
    FIND $%&DSTLett%=, ENVI &dstDRVforWIN=%&DSTNUM%! ENVI &dstDRVforWIN=%&DSTLett%
    LABE -left ,L26T16W290H31,把 %&srcDRVforWIN% 分区克隆到 %&dstDRVforWIN% 分区,,0xFF0000
    LABE -left ,L26T56W290H24,目标分区上的所有数据将会被覆盖！,,0x0000FF
    LABE ,L26T86W61H18,完成后：,,
    CHEK PCloneSHUT,L88T83W62H18,关机,CALL PCloneSHUTRB1,0
    CHEK PCloneRB,L152T83W62H18,重启,CALL PCloneSHUTRB2,0
    ITEM ,L120T128W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L220T128W80H28,取 消,KILL \,
_END

_SUB PCloneSHUTRB1
    FIND $%PCloneSHUT.Check%=1, ENVI @PCloneRB.Check=0
_END

_SUB PCloneSHUTRB2
    FIND $%PCloneRB.Check%=1, ENVI @PCloneSHUT.Check=0
_END

_SUB P2PDUMP
    MSTR &&SRCNUM,&&SRSLett=<1><2>%SPART%
    MSTR &&DSTNUM,&&DSTLett=<1><2>%DPART%
    FIND $%&SRCNUM%=%&DSTNUM%,TEAM MESS 源分区与目标分区相同！%&NLDD%%&NLDD%无法进行分区对拷！|EXIT _SUB
    IFEX $%&PEPOS% = 0,!!
    {
        FIND $%&SystemNumber%=%&DSTNUM%,TEAM MESS 目标分区为系统盘，要分区对拷，请在PE下进行。|EXIT _SUB
        FIND $%SYSTEMDRIVE%=%&DSTNUM%,TEAM MESS 目标分区为系统盘，要分区对拷，请在PE下进行。|EXIT _SUB
    }
    ENVI &&IsConfirm=0
    CALL ASKPartitionClone
    FIND $%&IsConfirm%=0, EXIT _SUB
    ENVI &&PartCPYNoUSB=
    CALL PartitionCopyNoUSB
    //动态磁盘部分
    FIND $%&SRSLett%=, TEAM ENVI &SRCDrvLett=%&SRCNUM%| CALL CheckISDynaimc 1 %&SRCNUM%! TEAM ENVI &SRCDrvLett=%&SRSLett%| CALL CheckISDynaimc 1 %&SRSLett%
    FIND $%&DSTLett%=, TEAM ENVI &DSTDrvLett=%&DSTNUM%| CALL CheckISDynaimc 2 %&DSTNUM%! TEAM ENVI &DSTDrvLett=%&DSTLett%| CALL CheckISDynaimc 2 %&DSTLett%
    ENVI @MHGHO2012.Visable=0
    ENVI &&RUNINFO1=
    EXEC* -exe:*#200 &RUNINFO1=!ghost.EXE -clone,mode=pcopy,src=%&SRCNUM%,dst=%&DSTNUM% -batch %&PartCPYNoIDE% %&PartCPYNoUSB% %paras%
    FIND $%&RUNINFO1%=,
    {
        MESS+icon102 对拷成功！@分区对拷 #OK *3000 $1
        FIND $%PCloneSHUT.Check%=1, ENVI &SHUTorREBOOT=1
        FIND $%PCloneRB.Check%=1, ENVI &SHUTorREBOOT=2
        ENVI @MHGHO2012.Visable=1
        KILL @MHGHO2012
        EXIT _SUB
    }
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    FILE ghstwarn.txt
    ENVI &&ERRPOS=0
    LPOS* &ERRPOS=T: 36002,1,%&RUNINFO1%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 用户终止，对拷失败！@分区对拷 #OK *5000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    FIND $%&DynCopy%=1,!!
    {
        ENVI &&RUNINFO2=0
        EXEC* -exe:*#200 &RUNINFO2=!ghost.EXE -clone,mode=pcopy,src=@OS:%&SRCDrvLett%,dst=@OS:%&DSTDrvLett% -batch %&PartCPYNoIDE% %&PartCPYNoUSB% %paras%
        FIND $%&RUNINFO2%=,
        {
            MESS+icon102 对拷成功！@分区对拷 #OK *3000 $1
            FIND $%PCloneSHUT.Check%=1, ENVI &SHUTorREBOOT=1
            FIND $%PCloneRB.Check%=1, ENVI &SHUTorREBOOT=2
            ENVI @MHGHO2012.Visable=1
            KILL @MHGHO2012
            EXIT _SUB
        }
        FILE ghost*.dmp
        FILE GHOSTERR.TXT
        LPOS* &ERRPOS=T: 36002,1,%&RUNINFO2%
        IFEX $%&ERRPOS% > 0,!!
        {
            MESS 用户终止，对拷失败！@分区对拷 #OK *5000 $1
            ENVI @MHGHO2012.Visable=1
            EXIT _SUB
        }
    }
    MESS 对拷失败！@分区对拷 #OK *3000 $1
    ENVI @MHGHO2012.Visable=1
_END

_SUB PartitionCopyNoUSB
    FIND $%&SRSLett%=, EXIT _SUB
    FIND $%&DSTLett%=, EXIT _SUB
    TEAM ENVI &&szPOS=0|ENVI &&srcDRV=|ENVI &&dstDRV=|ENVI &&srcBUS=|ENVI &&dstBUS=|ENVI &&A1=|ENVI &&A4=|ENVI &&vLn=
    LPOS &szPOS=:,1,%&SRCNUM%
    CALC #&szPOS = %&szPOS% - 1
    LSTR &srcDRV=%&szPOS%,%&SRCNUM%
    LPOS &szPOS=:,1,%&DSTNUM%
    CALC #&szPOS = %&szPOS% - 1
    LSTR &dstDRV=%&szPOS%,%&DSTNUM%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&srcDRV%, ENVI &srcBUS=%&A4%
        FIND $%&A1%=%&dstDRV%, ENVI &dstBUS=%&A4%
    }
    IFEX $%&srcBUS% = 7,! IFEX $%&dstBUS% = 7,! ENVI &PartCPYNoUSB=-nousb
_END

_SUB CheckISDynaimc
    ENVI &&letter=%2
    RSTR &&TOKEN=1,%&letter%
    FIND $%&TOKEN%=:,!EXIT _SUB
    ENVI &&SRCorDST=%1
    TEAM ENVI &&M=1|ENVI &&FTDRV=|ENVI &&IsDyn=
    LOOP #%&M% <= %&LnvFORM%,
    {
        ENVI @PARTMH:GHOSTABL.Val=?%&M%.2;&FTDRV
        FIND $%&FTDRV%=%&letter%, TEAM ENVI @PARTMH:GHOSTABL.Val=?%&M%.5;&IsDyn|EXIT LOOP
        CALC #&M = %&M% + 1
    }
    FIND $%IsDyn%=Dynamic,
    {
        ENVI &DynCopy=1
        FIND $%&DynOSVolume%=,CALL GetOSVolume
        FIND $%&DynOSVolume%=,EXIT _SUB
        TEAM ENVI &&V1=|ENVI &&V2=
        FORX *NL &DynOSVolume,&DynVol,
        {
             MSTR &V1,&V2=<1><2>%&DynVol%
             FIND $%&V2%=%&letter%,!!
             {
                 FIND $%&SRCorDST%=1,TEAM ENVI &SRCNUM=%&V1%|EXIT _SUB
                 FIND $%&SRCorDST%=2,TEAM ENVI &DSTNUM=%&V1%|EXIT _SUB
             }
        }
    }
_END

_SUB GHOSTCHECK
    ENVI  @GHOSTABL.Sel=?&&Sel
    ENVI  @GHOSTABL.Val=?%&Sel%.1;&PARTSEL1
    ENVI  @GHOSTABL.Val=?%&Sel%.2;&PARTSEL2
    ENVI  @GHOSTABL.Val=?%&Sel%.5;&PARTSEL5
    ENVI &DrvLettBackup=%&PARTSEL2%
    
    FIND $%&PARTSEL1%=  ,!
    {
        FIND $%&PARTSEL2%=  ,ENVI @STATUS2=所选分区：  序号 %&PARTSEL1%         无盘符!ENVI @STATUS2=所选分区：  序号 %&PARTSEL1%         盘符 %&PARTSEL2%
        CALL SetNOIDE
        EXIT _SUB
    }
    FIND $%&PARTSEL1%=  , ENVI  @STATUS2=所选分区：  %&PARTSEL2%
_END

_SUB SetNOIDE
    TEAM ENVI &&SPACOR=0|ENVI &&DRVNUMPICK=|ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=
    LPOS &SPACOR=:,1,%&PARTSEL1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DRVNUMPICK=%&SPACOR%,%&PARTSEL1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DRVNUMPICK%, TEAM ENVI &pBusType=%&A4%|EXIT FORX
    }
    FIND $%&pBusType%=3, ENVI @-:-:-:-:ADVANMH:advIDE.Check=0! ENVI @-:-:-:-:ADVANMH:advIDE.Check=1
_END

_SUB SetNOIDE2
    TEAM ENVI &&SPACOR=0|ENVI &&DRVNUMPICK=|ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=
    LPOS &SPACOR=:,1,%&PARTSEL1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DRVNUMPICK=%&SPACOR%,%&PARTSEL1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DRVNUMPICK%, TEAM ENVI &pBusType=%&A4%|EXIT FORX
    }
    FIND $%&pBusType%=3, ENVI @-:-:-:ADVANMH:advIDE.Check=0! ENVI @-:-:-:ADVANMH:advIDE.Check=1
_END

_SUB SetNOIDE3
    TEAM ENVI &&SPACOR=0|ENVI &&DRVNUMPICK=|ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=
    LPOS &SPACOR=:,1,%&PARTSEL1%
    CALC #&SPACOR= %&SPACOR% - 1
    LSTR &DRVNUMPICK=%&SPACOR%,%&PARTSEL1%
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&DRVNUMPICK%, TEAM ENVI &pBusType=%&A4%|EXIT FORX
    }
    FIND $%&pBusType%=3, ENVI @-:ADVANMH:advIDE.Check=0! ENVI @-:ADVANMH:advIDE.Check=1
_END

_SUB OnTimer1
    ENVI @PARTMH:INFO01=正在搜索镜像文件，请稍候...  已用时间: %&I%秒
    ENVI @HDMH:hINFO01=正在搜索镜像文件，请稍候...  已用时间: %&I%秒
    CALC #&I= %&I% + 1
_END

_SUB FINDGHO
    TEAM ENVI &&ANYGHO=|ENVI &&LSTEMP=|ENVI &&vln=|ENVI &&iPOS=|ENVI &&HD45=
    FORX *ab /S:1 /size:524288000:16106127360 \*.GHO,&ANYGHO,0,ENVI &LSTEMP=%&LSTEMP%%&NLDD%%&ANYGHO%          
    FORX *NL &LSTEMP,&vln,
     {
       FIND $%&vln%=,!
       {
          FNAM &HD45=%&vln%
          FIND $%&HD45%=HD4,! FIND $%&HD45%=HD5,! ENVI &GHOLS=%&GHOLS%|%&vln%
       }
     }
    MSTR &GHOLS=2,0,%&GHOLS% 
    RPOS &iPOS=|,1,%&GHOLS%
    CALC # &iPOS = %&iPOS% + 1
    MSTR &GHOLS1=%&iPOS%,0,%&GHOLS%
_END

_SUB FINDWIM
    TEAM ENVI &&ANYWIM=|ENVI &&R9=
    FORX *ab /S:1 /size:524288000:16106127360 \*.WIM,&ANYWIM,0,
    {
      FNAM &R9=%&ANYWIM%
      FIND $%&R9%=boot,! FIND $%&R9%=Winre,! ENVI &WIMLS=%&WIMLS%%&NLDD%%&ANYWIM% 
    } 
    ENVI &WIMLS=%&NLDD%%&WIMLS%      
_END

_SUB FINDESD
    ENVI &&ANYESD=
    FORX *ab /S:1 /size:524288000:16106127360 \*.ESD,&ANYESD,0,ENVI &ESDLS=%&ESDLS%%&NLDD%%&ANYESD% 
    ENVI &ESDLS=%&NLDD%%&ESDLS%
_END

_SUB FINDISO
    TEAM ENVI &&ANYISO=|ENVI &&ISODIR=
    FORX *ab /S:1 \*.ISO,&ANYISO,0,ENVI &ISOLS=%&ISOLS%%&NLDD%%&ANYISO%
    ENVI &ISOLS=%&NLDD%%&ISOLS%
_END

_SUB FINDGHOInCGIDir
    TEAM ENVI &&ANYGHO=|ENVI &&HD45=
    FORX %&CGIEXEDir%\*.GHO,&ANYGHO,0,CALL CutHD45
_END

_SUB CutHD45
    FNAM &HD45=%&ANYGHO%
    FIND $%&HD45%=HD4,! FIND $%&HD45%=HD5,! TEAM ENVI &CGIDirGHOList=%&CGIDirGHOList%%&ANYGHO%%&NLDD%|ENVI &CGIDirGHO=%&ANYGHO%
_END

_SUB FINDWIMInCGIDir
    TEAM ENVI &&ANYWIM=|ENVI &&BOOTWIM=
    FORX %&CGIEXEDir%\*.WIM,&ANYWIM,0,ENVI &CGIDirWIMList=%&CGIDirWIMList%%&ANYWIM%%&NLDD%
_END

_SUB FINDESDInCGIDir
    ENVI &&ANYESD=
    FORX %&CGIEXEDir%\*.ESD,&ANYESD,0,ENVI &CGIDirESDList=%&CGIDirESDList%%&ANYESD%%&NLDD%
_END

_SUB FreeDrvs
    TEAM ENVI &&Drv=|ENVI &&VD=
    FDRV &&OCUDrvs=*
    FORX * Z Y X W V U T S R Q P O N M L K J I H G F E D C B A,&Drv,
    {
        FORX * %&OCUDrvs%,&VD,FIND $%&Drv%=%&VD%,TEAM ENVI &FFDrv=|EXIT FORX!ENVI &FFDrv=%&Drv%
        FIND $%&FFDrv%=,!EXIT _SUB
    }
_END

//==========================  以下为操作硬盘  ================================================================
_SUB HDCHECK
    ENVI  @hTABL.Sel=?&&Sel
    ENVI  @hTABL.Val=?%&Sel%.1;&HDSEL
    ENVI  @hSTATUS2=所选硬盘：  %&HDSEL%
    ENVI  @hTABL.Val=?%&Sel%.2;&HDSizeSel
    ENVI  @hTABL.Val=?%&Sel%.3;&HDModelSel
    CALL SetHDIDE
_END

_SUB SetHDIDE
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&HDSEL%, TEAM ENVI &hBusType=%&A4%|EXIT FORX
    }
    FIND $%&hBusType%=3, ENVI @-:-:-:ADVANMH:advIDE.Check=0! ENVI @-:-:-:ADVANMH:advIDE.Check=1
_END

_SUB SetHDIDE2
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%&HDSEL%, TEAM ENVI &hBusType=%&A4%|EXIT FORX
    }
    FIND $%&hBusType%=3, ENVI @-:ADVANMH:advIDE.Check=0! ENVI @-:ADVANMH:advIDE.Check=1
_END

_SUB SethSTATUS4
    ENVI @hSTATUS4=源硬盘：      %SRCHD%
    CALL SetHDCOPYIDE
_END

_SUB SethSTATUS5
    ENVI @hSTATUS5=目标硬盘：    %DSTHD%
    CALL SetHDCOPYIDE
_END

_SUB SetHDCOPYIDE
    FIND $%DSTHD%=,EXIT _SUB
    FIND $%SRCHD%=,EXIT _SUB
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=|ENVI &&IsIDE1=0|ENVI &&IsIDE2=0
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%SRCHD%, TEAM ENVI &IsIDE1=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE1%=3, TEAM ENVI @-:-:-:ADVANMH:advIDE.Check=0|ENVI &HDCPYNoIDE=|EXIT _SUB
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%DSTHD%, TEAM ENVI &IsIDE2=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE2%=3, TEAM ENVI @-:-:-:ADVANMH:advIDE.Check=0|ENVI &HDCPYNoIDE=|EXIT _SUB! TEAM ENVI @-:-:-:ADVANMH:advIDE.Check=1|ENVI &HDCPYNoIDE=-noide
_END

_SUB SetHDCOPYIDE2
    FIND $%DSTHD%=,EXIT _SUB
    FIND $%SRCHD%=,EXIT _SUB
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A4=|ENVI &&IsIDE1=0|ENVI &&IsIDE2=0
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%SRCHD%, TEAM ENVI &IsIDE1=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE1%=3, TEAM ENVI @-:ADVANMH:advIDE.Check=0|ENVI &HDCPYNoIDE=|EXIT _SUB
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%DSTHD%, TEAM ENVI &IsIDE2=%&A4%|EXIT FORX
    }
    FIND $%&IsIDE2%=3, TEAM ENVI @-:ADVANMH:advIDE.Check=0|ENVI &HDCPYNoIDE=|EXIT _SUB! TEAM ENVI @-:ADVANMH:advIDE.Check=1|ENVI &HDCPYNoIDE=-noide
_END

_SUB hRESPATH
    BROW &&hREPATH,,请选择镜像文件,GHO文件和ISO文件(*.GHO;*.ISO)|*.GHO;*.ISO,
    FIND $%&hREPATH%=,!
    {
        FIND $%&hREPATH%=%&DLIST1ITEM%,ENVI @hLIST.SEL=%&hREPATH%!ENVI @hLIST.ADDSEL=%&hREPATH%
        ENVI. @hSTATUS3=所选路径/文件：%hLIST%
        FEXT &&hEXT=%hLIST%
        FIND $%&hEXT%=ISO,TEAM ENVI &ahCHECK=2|CALL GICHECK "%hLIST%"
    }
_END

_SUB hBACKPATH
    BROW &&hBKPATH,&D:\SYSTEM.GHO,请选择保存目录,GHO文件(*.GHO)|*.GHO|所有文件(*.*)|*.*,
    FIND $%&hBKPATH%=,!
    {
        // PECMD2012的BUG，通过【浏览】按钮添加文件时，当要添加的文件本来在下拉框就已存在
        // 且为第一个条目时，程序会退出。以下是为修正此BUG的。
        ENVI @hBACK.QUERY=&&AllBKGHO
        FIND $%&AllBKGHO%=,! ENVI @hBACK.QUERY=1;&&FirstBKGHO
        FIND $%&hBKPATH%=%&FirstBKGHO%, ENVI @hBACK.SEL=%&hBKPATH%! ENVI @hBACK.ADDSEL=%&hBKPATH%
        ENVI. @hSTATUS3=所选路径/文件：%hBACK%
    }
_END

_SUB HDVIS1
    ENVI @hRETIP=3.请选择镜像文件：
    ENVI @hBACK.Visable=0
    ENVI @hBkBn.Visable=0
    ENVI @hLIST.Visable=1
    ENVI @hReBn.Visable=1
    ENVI @hSTATUS1=所选操作：还原硬盘
    ENVI. @hSTATUS3=所选路径/文件：%hLIST%
    ENVI @hLABE.Visable=1
    ENVI @hLABLE.Visable=0
    ENVI @SRCHD.Visable=0
    ENVI @DSTHD.Visable=0
    ENVI @hSTATUS2.Visable=1
    ENVI @hSTATUS4.Visable=0
    ENVI @hSTATUS3.Visable=1
    ENVI @hSTATUS5.Visable=0
    CALL SetHDIDE
_END

_SUB HDVIS2
    ENVI @hRETIP=3.请选择保存路径：
    ENVI @hLIST.Visable=0
    ENVI @hReBn.Visable=0
    ENVI @hBACK.Visable=1
    ENVI @hBkBn.Visable=1
    ENVI @hSTATUS1=所选操作：备份硬盘
    ENVI. @hSTATUS3=所选路径/文件：%hBACK%
    ENVI @hLABE.Visable=1
    ENVI @hLABLE.Visable=0
    ENVI @SRCHD.Visable=0
    ENVI @DSTHD.Visable=0
    ENVI @hSTATUS2.Visable=1
    ENVI @hSTATUS4.Visable=0
    ENVI @hSTATUS3.Visable=1
    ENVI @hSTATUS5.Visable=0
    CALL SetHDIDE
_END

_SUB HDVIS3
    ENVI @hRETIP=2.请选择源硬盘：
    ENVI @hLIST.Visable=0
    ENVI @hReBn.Visable=0
    ENVI @hBACK.Visable=0
    ENVI @hBkBn.Visable=0
    ENVI @hLABE.Visable=0
    ENVI @hLABLE.Visable=1
    ENVI @SRCHD.Visable=1
    ENVI @DSTHD.Visable=1
    ENVI @hSTATUS1=所选操作：硬盘对拷
    ENVI @hSTATUS2.Visable=0
    ENVI @hSTATUS4.Visable=1
    ENVI @hSTATUS4=源硬盘：      %SRCHD%
    ENVI @hSTATUS3.Visable=0
    ENVI @hSTATUS5.Visable=1
    ENVI @hSTATUS5=目标硬盘：    %DSTHD%
    CALL SetHDCOPYIDE
_END

_SUB hREORBK
    FIND $%hRERADI.Check%=0,!!FIND $%hBKRADI.Check%=0,!!FIND $%HD2HD.Check%=0,!!TEAM MESS 您还没有选择操作！%&NLDD%%&NLDD%请选择【还原硬盘】、【备份硬盘】或【硬盘对拷】！|EXIT _SUB
    FIND $%HD2HD.Check%=0,!!
    {
        FIND $%&HDSEL%=, TEAM MESS 您还没有选择硬盘！%&NLDD%%&NLDD%请选择硬盘！|EXIT _SUB
        FIND $%hRERADI.Check%=1,
        {
            RSTR &&REL4=4,%hSTATUS3%
            FIND $%&REL4%=.GHO,!
            {
                FIND $%&REL4%=.ISO, TEAM MESS. 您当前选的是%hLIST%文件，%&NLDD%%&NLDD%请再选一下此ISO文件，看其中有没有您需要的GHO镜像！|EXIT _SUB
                TEAM MESS 您还没有选择GHO镜像！|EXIT _SUB
            }
            CALL hREGHOST
        }
        FIND $%hBKRADI.Check%=1,
        {
            MSTR &&BKBLANK=<1>%hBACK%
            FIND $%&BKBLANK%=,TEAM MESS 您还没有选择保存路径！|EXIT _SUB
            CALL hBKGHOST
        }
    }
    FIND $%HD2HD.Check%=1,!!
    {
        FIND $%SRCHD%=,TEAM MESS 您还没有选择源硬盘！|EXIT _SUB
        FIND $%DSTHD%=,TEAM MESS 您还没有选择目标硬盘！|EXIT _SUB
        CALL HD2HDCOPY
    }
_END

_SUB hREGHOST
    TEAM ENVI &&hhDRV=|ENVI &&hFsame=|ENVI &&hDrvNUM=
    FDRV &&hREDrv=%hLIST%
    FORX *NL &vFORM,&hFsame,
    {
        MSTR &hhDRV=<2>%&hFsame%
        FIND $%&hhDRV%=%&hREDrv%, TEAM MSTR &hDrvNUM=<1>%&hFsame%|EXIT FORX
    }
    LPOS &&hdPOS=:,1,%&hDrvNUM%
    CALC #&hdPOS = %&hdPOS% - 1
    LSTR &hDrvNUM=%&hdPOS%,%&hDrvNUM%
    FIND $%&hDrvNUM%=%&HDSEL%,
    {
        FEXT &&hdEXT=%hLIST%
        FIND $%&hdEXT%=ISO, TEAM MESS ISO文件在目标硬盘，无法还原！%&NLDD%%&NLDD%可将它复制到其它硬盘再进行还原。|EXIT _SUB
        TEAM MESS GHO镜像在目标硬盘，无法还原！%&NLDD%%&NLDD%可将它复制到其它硬盘再进行还原。|EXIT _SUB
    }
    LPOS &&hPOS=：,1,%hSTATUS3%
    CALC #&hPOS = %&hPOS% + 1
    MSTR &&hFILE=%&hPOS%,0,%hSTATUS3%
    FEXT &&hdEXT=%hLIST%
    FIND $%&hdEXT%=ISO, CALL LoadISO "%hLIST%"
    TEAM ENVI &&szNoIDE=| ENVI &&szNoUSB=| ENVI &&hCRC=| ENVI &&PWDRE=
    CALL CRPWD "%&hFILE%"
    CALL GetNoIDENoUSB %hBusType% %&hREDrv%
    FIND $%advCRC.Check%=1, ENVI &hCRC=-crcignore
    IFEX %&hFILE%, TEAM CALL OnResHD|EXIT _SUB
    MESS 找不到所选GHO镜像！
_END

_SUB ASKHDRestore,W432H178,还原硬盘,,#1,,
    ENVI &&HDInfo=
    CALL SetHDInfoString
    LABE. -left ,L26T16W400H18,把"%&hFILE%"还原到,,0xFF0000
    LABE -left ,L26T36W400H18,磁盘%&HDSEL%  （%&HDInfo%）,,0xFF0000
    LABE ,L26T68W61H18,完成后：,,
    CHEK HDRestoreSHUT,L88T65W62H18,关机,CALL HDRestoreSHUTRB1,0
    CHEK HDRestoreRB,L152T65W62H18,重启,CALL HDRestoreSHUTRB2,0
    ITEM ,L220T102W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L320T102W80H28,取 消,KILL \,
_END

_SUB SetHDInfoString
    TEAM ENVI &&A1=|ENVI &&A2=|ENVI &&A3=
    MSTR &A1,&A2,&A3=<1><2><3>%&HDModelSel%
    FIND $%&A3%=,! TEAM ENVI &HDInfo=%&HDSizeSel%，%&A1% %&A2% %&A3%|EXIT _SUB
    FIND $%&A2%=,! TEAM ENVI &HDInfo=%&HDSizeSel%，%&A1% %&A2%|EXIT _SUB
    FIND $%&A1%=,! TEAM ENVI &HDInfo=%&HDSizeSel%，%&A1%|EXIT _SUB
    ENVI &HDInfo=%&HDSizeSel%
_END

_SUB HDRestoreSHUTRB1
    FIND $%HDRestoreSHUT.Check%=1, ENVI @HDRestoreRB.Check=0
_END

_SUB HDRestoreSHUTRB2
    FIND $%HDRestoreRB.Check%=1, ENVI @HDRestoreSHUT.Check=0
_END

_SUB OnResHD
    IFEX $%&PEPOS% = 0,!! FIND $%&HDSEL%=%&SysDrvNum%,!! TEAM MESS 请到PE中还原系统硬盘。|EXIT _SUB
    ENVI &&IsConfirm=0
    CALL ASKHDRestore
    FIND $%&IsConfirm%=0, EXIT _SUB
    ENVI @MHGHO2012.Visable=0
    ENVI &&RUNINFO=0
    EXEC* -exe:*#200 &RUNINFO=!ghost.EXE -clone,mode=load,src="%&hFILE%",dst=%&HDSEL% -batch %&szNoIDE% %&szNoUSB% %&hCRC% %&PWDRE% %paras%
    FIND $%&RUNINFO%=,
    {
        MESS+icon102 还原成功！@还原硬盘 #OK *3000 $1
        FIND $%HDRestoreSHUT.Check%=1, ENVI &SHUTorREBOOT=1
        FIND $%HDRestoreRB.Check%=1, ENVI &SHUTorREBOOT=2
        ENVI @MHGHO2012.Visable=1
        KILL @MHGHO2012
        EXIT _SUB
    }
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    FILE ghstwarn.txt
    ENVI &&ERRPOS=0
    LPOS* &ERRPOS=T: 36002,1,%&RUNINFO%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 用户终止，还原失败！@还原硬盘 #OK *5000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    MESS 还原失败！@还原硬盘 #OK *3000 $1
    ENVI @MHGHO2012.Visable=1
_END

_SUB ASKHDBackup,W432H178,备份硬盘,,#1,,
    ENVI &&HDInfo=
    CALL SetHDInfoString
    LABE -left ,L26T16W400H18,把磁盘%&HDSEL%  （%&HDInfo%）,,0xFF0000
    LABE. -left ,L26T36W400H18,备份到"%&hBKDir%",,0xFF0000
    LABE ,L26T68W61H18,完成后：,,
    CHEK HDBackupSHUT,L88T65W62H18,关机,CALL HDBackupSHUTRB1,0
    CHEK HDBackupRB,L152T65W62H18,重启,CALL HDBackupSHUTRB2,0
    ITEM ,L220T102W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L320T102W80H28,取 消,KILL \,
_END

_SUB HDBackupSHUTRB1
    FIND $%HDBackupSHUT.Check%=1, ENVI @HDBackupRB.Check=0
_END

_SUB HDBackupSHUTRB2
    FIND $%HDBackupRB.Check%=1, ENVI @HDBackupSHUT.Check=0
_END

_SUB ASKExistHDBackup,W432H198,备份硬盘,,#1,,
    ENVI &&HDInfo=
    CALL SetHDInfoString
    LABE -left ,L26T16W400H18,把磁盘%&HDSEL%  （%&HDInfo%）,,0xFF0000
    LABE. -left ,L26T36W400H18,备份到"%&hBKDir%",,0xFF0000
    LABE. -left ,L26T60W400H18,将覆盖原有的备份文件！,,0x0000FF
    LABE ,L26T88W61H18,完成后：,,
    CHEK ExistHDBackupSHUT,L88T85W62H18,关机,CALL ExistHDBackupSHUTRB1,0
    CHEK ExistHDBackupRB,L152T85W62H18,重启,CALL ExistHDBackupSHUTRB2,0
    ITEM ,L220T122W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L320T122W80H28,取 消,KILL \,
_END

_SUB ExistHDBackupSHUTRB1
    FIND $%ExistHDBackupSHUT.Check%=1, ENVI @ExistHDBackupRB.Check=0
_END

_SUB ExistHDBackupSHUTRB2
    FIND $%ExistHDBackupRB.Check%=1, ENVI @ExistHDBackupSHUT.Check=0
_END

_SUB hBKGHOST
    MSTR &&hBLK=<1->%hBACK%
    LSTR &&hBKDrv=2,%&hBLK%
    TEAM ENVI &&hFBK=| ENVI &&hBDrvNUM=
    FORX *NL &vFORM,&hFBK,
    {
        MSTR &&iBKDrv=<2>%&hFBK%
        FIND $%&iBKDrv%=%&hBKDrv%, TEAM MSTR &hBDrvNUM=<1>%&hFBK%|EXIT FORX
    }
    LPOS &&hBPOS=:,1,%&hBDrvNUM%
    CALC #&hBPOS = %&hBPOS% - 1
    LSTR &hBDrvNUM=%&hBPOS%,%&hBDrvNUM%
    FIND $%&hBDrvNUM%=%&HDSEL%, TEAM MESS 无法把备份文件保存到要备份的硬盘！%&NLDD%%&NLDD%请重新选择保存路径！|EXIT _SUB
    ENVI &&hBKDir=
    RSTR &&BKL4=4,%&hBLK%
    FIND $%&BKL4%=.GHO, ENVI &hBKDir=%&hBLK%! ENVI &hBKDir=%&hBLK%.GHO
    RPOS &&hDIR=\,1,%&hBKDir%
    LSTR &&hMKDIR=%&hDIR%,%&hBKDir%
    ENVI &&ExistFolder=0
    IFEX %&hMKDIR%, ENVI &ExistFolder=1!MDIR %&hMKDIR%
    FIND $%HideFolder.Check%=1, IFEX %&hMKDIR%, SITE %&hMKDIR%,+H
    MSTR &&hSIZE=<1>%advBL02%
    TEAM ENVI &&szNoIDE=| ENVI &&szNoUSB=| ENVI &&BKPWD=| ENVI &&hCMPR=-z1| ENVI &&hSPLIT=-split=%&hSIZE%
    FIND $%advPWD1.Check%=1,
    {
        FIND $%advEDIT1%=,!
        {
            TEAM ENVI &&realPWD=|ENVI &&PL=
            ENVI &realPWD=%advEDIT1%
            STRL &PL=%&realPWD%
            IFEX $%&PL% > 10, LSTR &realPWD=10,%&realPWD%
            ENVI &BKPWD=-pwd="%&realPWD%"
        }
    }
    CALL GetNoIDENoUSB %hBusType% %&hBKDrv%
    FIND $%advBL01%=不压缩, ENVI &hCMPR=
    FIND $%advBL01%=高压缩, ENVI &hCMPR=-z3
    FIND $%advBL01%=极限压缩, ENVI &hCMPR=-z9
    FIND $%advBL02%=不分卷, ENVI &hSPLIT=-split=0
    FIND $%advBL02%=自动检测, ENVI &hSPLIT=
    TEAM ENVI &&IsConfirm=0|ENVI &&dstFileExist=0
    IFEX %&hBKDir%, TEAM ENVI &dstFileExist=1|CALL ASKExistHDBackup! CALL ASKHDBackup
    FIND $%&IsConfirm%=0,
    {
        IFEX $%&ExistFolder% = 0,!!
        {
            MSTR &&hKillDir=-2,0,%&hMKDIR%
            SITE %&hKillDir%,-H-S-R
            PATH #%&hKillDir%
        }
        EXIT _SUB
    }
    TEAM ENVI &&iTIME=|ENVI &&NewGHOTime=0|ENVI &&NewGHOSize=0
    TEAM ENVI &&T1=|ENVI &&T2=|ENVI &&T3=|ENVI &&T4=|ENVI &&T5=|ENVI &&T6=|ENVI &&T7=
    ENVI &OldGHOExist=0
    IFEX %&hBKDir%,
    {
        ENVI &OldGHOExist=1
        SITE ?-local ,&iTIME=FTIME,%&hBKDir%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &OldGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    ENVI @MHGHO2012.Visable=0
    TEAM ENVI &&RUNINFO=0|ENVI &&report=0
    EXEC* -exe:*#200 &RUNINFO=!ghost.EXE -clone,mode=dump,src=%&HDSEL%,dst="%&hBKDir%" -batch %&szNoIDE% %&szNoUSB% %&BKPWD% %&hCMPR% %&hSPLIT% %paras%
    IFEX %&hBKDir%,
    {
        SIZE &NewGHOSize=%&hBKDir%
        SITE ?-local ,&iTIME=FTIME,%&hBKDir%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &NewGHOTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    FIND $%&RUNINFO%=,
    {
        IFEX %&hBKDir%,!!
        {
            IFEX $%&OldGHOExist% = 1,!!
            {
                FIND $%&NewGHOTime%=%&OldGHOTime%, TEAM ENVI &report=1|MESS 备份失败！ @备份硬盘 #OK *3000 $1
                FIND $%&NewGHOTime%=%&OldGHOTime%,!
                {
                    IFEX $%&NewGHOSize% = 0, TEAM ENVI &report=1|MESS 备份失败！ @备份硬盘 #OK *3000 $1
                    IFEX $%&NewGHOSize% = 0,!
                    {
                        MESS+icon102 备份成功！@备份硬盘 #OK *3000 $1
                        IFEX $%&dstFileExist% = 0,!!
                        {
                            FIND $%HDBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                            FIND $%HDBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                        }
                        IFEX $%&dstFileExist% = 1,!!
                        {
                            FIND $%ExistHDBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                            FIND $%ExistHDBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                        }
                        ENVI @MHGHO2012.Visable=1
                        KILL @MHGHO2012
                        EXIT _SUB
                    }
                }
            }
            IFEX $%&OldGHOExist% = 0,!!
            {
                IFEX $%&NewGHOSize% = 0, TEAM ENVI &report=1|MESS 备份失败！ @备份硬盘 #OK *3000 $1
                IFEX $%&NewGHOSize% = 0,!
                {
                    MESS+icon102 备份成功！@备份硬盘 #OK *3000 $1
                    IFEX $%&dstFileExist% = 0,!!
                    {
                        FIND $%HDBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                        FIND $%HDBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                    }
                    IFEX $%&dstFileExist% = 1,!!
                    {
                        FIND $%ExistHDBackupSHUT.Check%=1, ENVI &SHUTorREBOOT=1
                        FIND $%ExistHDBackupRB.Check%=1, ENVI &SHUTorREBOOT=2
                    }
                    ENVI @MHGHO2012.Visable=1
                    KILL @MHGHO2012
                    EXIT _SUB
                }
            }
        }
        IFEX %&hBKDir%,! TEAM ENVI &report=1|MESS 备份失败！ @备份硬盘 #OK *3000 $1
    }
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    FILE ghstwarn.txt
    FIND $%&NewGHOTime%=%&OldGHOTime%,! FILE %&hBKDir%
    IFEX $%&ExistFolder% = 0,!!
    {
        MSTR &&hKillDir=-2,0,%&hMKDIR%
        SITE %&hKillDir%,-H-S-R
        PATH #%&hKillDir%
    }
    ENVI &&ERRPOS=0
    LPOS* &ERRPOS=T: 651,1,%&RUNINFO%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 保存镜像的分区空间不足，备份失败！@备份硬盘 #OK *10000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    LPOS* &ERRPOS=T: 519,1,%&RUNINFO%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 保存镜像的分区空间不足，备份失败！@备份硬盘 #OK *10000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    LPOS* &ERRPOS=T: 36002,1,%&RUNINFO%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 用户终止，备份失败！@备份硬盘 #OK *5000 $1
        ENVI @MHGHO2012.Visable=1
        EXIT _SUB
    }
    IFEX $%&report% = 0, MESS 备份失败！@备份硬盘 #OK *3000 $1
    ENVI @MHGHO2012.Visable=1
_END

_SUB HD2HDCOPY
    FIND $%SRCHD%=%DSTHD%,TEAM MESS 源硬盘与目标硬盘相同！%&NLDD%%&NLDD%无法进行硬盘对拷！|EXIT _SUB
    IFEX $%&PEPOS% = 0,!!
    {
        FIND $%&SysDrvNum%=%DSTHD%,TEAM MESS 目标硬盘是系统硬盘，要硬盘对拷，请到PE中进行。|EXIT _SUB
    }
    ENVI &&IsConfirm=0
    CALL ASKHDCopy
    FIND $%&IsConfirm%=0, EXIT _SUB
    ENVI &&HDCPYNoUSB=
    CALL GetHDCopyNoUSB
    ENVI @MHGHO2012.Visable=0
    EXEC* -exe:*#200 &&RUNINFO=!ghost.EXE -clone,mode=copy,src=%SRCHD%,dst=%DSTHD% -batch %&HDCPYNoIDE% %&HDCPYNoUSB% %paras%
    FIND $%&RUNINFO%=,
    {
        MESS+icon102 对拷成功！@硬盘对拷 #OK *3000 $1
        FIND $%HDCopySHUT.Check%=1, ENVI &SHUTorREBOOT=1
        FIND $%HDCopyRB.Check%=1, ENVI &SHUTorREBOOT=2
        ENVI @MHGHO2012.Visable=1
        KILL @MHGHO2012
        EXIT _SUB
    }
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    FILE ghstwarn.txt
    MESS 对拷失败！@硬盘对拷 #OK *3000 $1
    ENVI @MHGHO2012.Visable=1
_END

_SUB ASKHDCopy,W432H208,硬盘对拷,,#1,,
    TEAM ENVI &&srcHDInfo=|ENVI &&dstHDInfo=|ENVI &&HDInfo=
    CALL GetHDInformation %SRCHD%
    ENVI &srcHDInfo=%&HDInfo%
    ENVI &HDInfo=
    CALL GetHDInformation %DSTHD%
    ENVI &dstHDInfo=%&HDInfo%
    LABE -left ,L26T16W400H18,把磁盘%SRCHD% （%&srcHDInfo%）克隆到,,0xFF0000
    LABE -left ,L26T36W400H18,磁盘%DSTHD% （%&dstHDInfo%）,,0xFF0000
    LABE -left ,L26T66W400H18,目标磁盘上的所有数据将会被覆盖！,,0x0000FF
    LABE ,L26T98W61H18,完成后：,,
    CHEK HDCopySHUT,L88T95W62H18,关机,CALL HDCopySHUTRB1,0
    CHEK HDCopyRB,L152T95W62H18,重启,CALL HDCopySHUTRB2,0
    ITEM ,L220T132W80H28,确 定,TEAM ENVI &IsConfirm=1|KILL \,
    ITEM ,L320T132W80H28,取 消,KILL \,
_END

_SUB HDCopySHUTRB1
    FIND $%HDCopySHUT.Check%=1, ENVI @HDCopyRB.Check=0
_END

_SUB HDCopySHUTRB2
    FIND $%HDCopyRB.Check%=1, ENVI @HDCopySHUT.Check=0
_END

_SUB GetHDInformation
    TEAM ENVI &&A1=|ENVI &&A2=|ENVI &&A3=|ENVI &&szHDSize=|ENVI &&szHDModel=|ENVI &&vLn=|ENVI &&HDNum=
    ENVI &HDNum=%1
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A2,&A3=<1><2><3>%&vLn%
        FIND $%&A1%=%&HDNum%, TEAM ENVI &szHDSize=%&A2%|ENVI &szHDModel=%&A3%|EXIT FORX
    }
    MSTR &A1,&A2,&A3=<1><2><3>%&szHDModel%
    FIND $%&A3%=,! TEAM ENVI &HDInfo=%&szHDSize%，%&A1% %&A2% %&A3%|EXIT _SUB
    FIND $%&A2%=,! TEAM ENVI &HDInfo=%&szHDSize%，%&A1% %&A2%|EXIT _SUB
    FIND $%&A1%=,! TEAM ENVI &HDInfo=%&szHDSize%，%&A1%|EXIT _SUB
    ENVI &HDInfo=%&szHDSize%
_END

_SUB GetHDCopyNoUSB
    TEAM ENVI &&srcBUS=|ENVI &&dstBUS=|ENVI &&A1=|ENVI &&A4=|ENVI &&vLn=
    FORX *NL &HDMHINFO,&vLn,
    {
        MSTR* &A1,&A4=<1><4>%&vLn%
        FIND $%&A1%=%SRCHD%, ENVI &srcBUS=%&A4%
        FIND $%&A1%=%DSTHD%, ENVI &dstBUS=%&A4%
    }
    IFEX $%&srcBUS% = 7,! IFEX $%&dstBUS% = 7,! ENVI &HDCPYNoUSB=-nousb
_END

//====================================== 以下为“高级” ============================================================
_SUB EnablePWD
    FIND $%advPWD1.Check%=1,ENVI @advEDIT1.Enable=1!ENVI @advEDIT1.Enable=0
_END

_SUB advPATH
    BROW &&advP,,请选择镜像文件,GHO和ISO文件(*.GHO;*.ISO)|*.GHO;*.ISO,
    FIND $%&advP%=,!
    {
        FIND $%&advP%=%&ILIST1ITEM%,ENVI @advLIST.SEL=%&advP%!ENVI @advLIST.ADDSEL=%&advP%
        ENVI. @advLABE=所选文件：%advLIST%
        FEXT &&advEXT=%advLIST%
        FIND $%&advEXT%=ISO,TEAM ENVI &ahCHECK=3|CALL GICHECK "%advLIST%"
    }
_END

_SUB IntegCheck
    RSTR &&advChExt=4,%advLABE%
    FIND $%&advChExt%=.ISO,TEAM MESS 您选择的不是GHO镜像文件！|EXIT _SUB
    LPOS &&aPOS=：,1,%advLABE%
    CALC #&aPOS = %&aPOS% + 1
    MSTR &&aFILE=%&aPOS%,0,%advLABE%
    IFEX %&aFILE%,TEAM CALL CHKINTGR "%&aFILE%"|EXIT _SUB
    MESS 找不到所选GHO镜像！
_END

_SUB CHKINTGR
    ENVI &&PWDRE=
    ENVI &&iPath=%1
    CALL CRPWD %&iPath%
    ENVI &&ERRINFO=0
    EXEC* -exe:*#200 &ERRINFO=!ghost.EXE -chkimg,%1 -batch %&PWDRE%
    FIND $%&ERRINFO%=,TEAM MESS.+icon102 %~1 镜像完整！| EXIT _SUB
    FILE ghost*.dmp
    FILE GHOSTERR.TXT
    ENVI &&ERRPOS=0
    LPOS* &ERRPOS=T: 36002,1,%&ERRINFO%
    IFEX $%&ERRPOS% > 0,!!
    {
        MESS 用户终止！@检查GHO镜像是否完整 #OK *3000 $1
        EXIT _SUB
    }
    MESS.+icon7 %~1 镜像不完整！
_END

_SUB paraHELP,W432H344,参数帮助,,#1
    ENVI &&PrmTITLE=120:参数%&TAB%268:说明
    ENVI &&PrmDATA=-nousb%&TAB%禁用访问USB设备%&NLHH%-no1394%&TAB%禁用访问1394设备%&NLHH%-noscsi%&TAB%禁用访问SCSI设备%&NLHH%-fro%&TAB%强制拷贝有坏簇的分区%&NLHH%-forceusb%&TAB%启用内置USB设备驱动%&NLHH%-force1394%&TAB%启用内置1394设备驱动%&NLHH%-ia%&TAB%完全执行扇区到扇区的复制%&NLHH%-id%&TAB%完全复制整个硬盘，包括未划分的空间
    LABE ,L14T10W402H16,您可以输入如下的参数，多个参数用空格分隔：,,
    LABE ,L14T30W380H16,    -nousb -fro,,
    LABE ,L14T50W402H16,也可以从以下选择，或者部分手动输入部分从以下选择。,,
    TABL PrmTabl,L12T70W402H142,%&PrmTITLE%,%&PrmDATA%,0x82600
    LABE -left ,L18T220W400H40,提示：本一键恢复支持的参数不限于以上列出的，凡是GHOST支持的，它都支持。,,0xFF0000,
    ITEM ,L226T270W80H28,确 定,TEAM CALL PrmPick|KILL \,
    ITEM ,L326T270W80H28,关 闭,KILL \,
_END

_SUB PrmPick
    ENVI @PrmTabl.Check=?*&&PrmPs
    FIND $%&PrmPs%=,!
    {
        TEAM ENVI &&ParaSEL=| ENVI &&LPick=| ENVI &&PPS=
        FORX * %&PrmPs%,&LPick,
        {
            ENVI @PrmTabl.Val=?%&LPick%.1;&ParaSEL
            ENVI &PPS=%&PPS% %&ParaSEL%
        }
        ENVI &PPS=%paras%%&PPS%
        ENVI @-:-:-:ADVANMH:paras=%&PPS%
    }
_END

_SUB DOITph
    ENVI @DOIT1.Enable=0
    ENVI &&M=0
    LOOP #%&BasicDone% = 0,
    {
        WAIT 1000
        CALC #&M = %&M% + 1
        IFEX $%&M% > 10, EXIT LOOP
    }
    IFEX $%&BasicDone% = 0, TEAM MESS 系统繁忙，请稍后再试。|ENVI @DOIT1.Enable=1|EXIT _SUB
    ENVI @DOIT1.Enable=1
    FIND $%&TABS1.Select%=1,TEAM CALL REORBK|EXIT _SUB
    FIND $%&TABS1.Select%=2,CALL hREORBK
_END

_SUB CRPWD
    EXEC* -exe:*#603 &&PWDINFO=!GP.EXE %1
    FIND $%&PWDINFO%=,!ENVI &PWDRE=-pwd="%&PWDINFO%"
_END

_SUB DISPTIP
    ENVI &&CTRLNUM=%1
    FIND $%&CTRLNUM%=1,
    {
        FIND $%BKRADI.Check%=1,EXIT _SUB
        ENVI &&SHOWINFO=%STATUS3%
        LPOS* &&arrowPOS=->,1,%&SHOWINFO%
        IFEX $%&arrowPOS% > 0, TEAM CALL SHOWWIMTIPS|EXIT _SUB
        ENVI &&LFILE=%GHOLIST% 
        TEAM CALL SHOWTIPS|EXIT _SUB
    }
    FIND $%&CTRLNUM%=2,
    {
        FIND $%hBKRADI.Check%=1,EXIT _SUB
        ENVI &&SHOWINFO=%hSTATUS3%
        ENVI &&LFILE=%hLIST%
        TEAM CALL SHOWTIPS|EXIT _SUB
    }
    FIND $%&CTRLNUM%=3,
    {
        ENVI &&SHOWINFO=%advLABE%
        ENVI &&LFILE=%advLIST%
        CALL SHOWTIPS
    }
_END

_SUB SHOWWIMTIPS
    ENVI @@Cur=?&&CurX;&&CurY
    LPOS &&fPOS=：,1,%&SHOWINFO%
    CALC #&fPOS = %&fPOS% + 1
    MSTR &&fFILE=%&fPOS%,0,%&SHOWINFO%
    LPOS* &&wPOS=->,1,%&fFILE%
    CALC #&wPOS = %&wPOS% - 1
    LSTR &&wFILE=%&wPOS%,%&fFILE%
    SIZE &&iSize=%&wFILE%
    CALC &iSize = %&iSize% /1048576#2
    IFEX $%&iSize% > 999, TEAM CALC &iSize = %&iSize% /1024#2|ENVI &iSize=%&iSize% GB! ENVI &iSize=%&iSize% MB
    SITE ?-local ,&&iTIME=FTIME,%&wFILE%
    MSTR &T1,&T2,&T3,&T4,&T5,&T6=<1><2><3><4><5><6>%&iTIME%
    ENVI &iTIME=%&T1%年%&T2%月%&T3%日 %&T4%:%&T5%:%&T6%
    ENVI &&szInfo=%&wFILE%%&NLDD%大小： %&iSize%%&NLDD%修改时间：%&iTIME%
    TIPS. ,%&fFILE%%&NLDD%%&NLDD%%&szInfo%,5000,0,@AL%&CurX%T%&CurY%
_END

_SUB SHOWTIPS
    FIND $%&LFILE%=, EXIT _SUB
    TEAM ENVI &&T1=|ENVI &&T2=|ENVI &&T3=|ENVI &&T4=|ENVI &&T5=|ENVI &&T6=|ENVI &&T21=|ENVI &&T22=
    ENVI @@Cur=?&&CurX;&&CurY
    LPOS &&fPOS=：,1,%&SHOWINFO%
    CALC #&fPOS = %&fPOS% + 1
    MSTR &&fFILE=%&fPOS%,0,%&SHOWINFO%
    SIZE &&iSize=%&fFILE%
    CALC &iSize = %&iSize% /1048576#2
    IFEX $%&iSize% > 999, TEAM CALC &iSize = %&iSize% /1024#2|ENVI &iSize=%&iSize% GB! ENVI &iSize=%&iSize% MB
    SITE ?-local ,&&iTIME=FTIME,%&fFILE%
    MSTR &T1,&T2,&T3,&T4,&T5,&T6=<1><2><3><4><5><6>%&iTIME%
    ENVI &iTIME=%&T1%年%&T2%月%&T3%日 %&T4%:%&T5%:%&T6%
    ENVI &&szInfo=%&fFILE%%&NLDD%大小： %&iSize%%&NLDD%修改时间：%&iTIME%
    TIPS. ,%&szInfo%,5000,0,@AL%&CurX%T%&CurY%
_END

// =======================  WIM 模块  =====================================================================

_SUB WIMGICHECK
    FEXT &&EXT=%~1
    FIND $%&EXT%=WIM, TEAM CALL VolumeInWIM %1|EXIT _SUB
    FIND $%&EXT%=ESD, TEAM CALL VolumeInWIM %1|EXIT _SUB
    FIND $%&EXT%=SWM, TEAM CALL VolumeInWIM %1|EXIT _SUB
    FIND $%&EXT%=ISO, CALL GHOWIMinISO %1
_END

_SUB VolumeInWIM,W600H470,WIM&ESD镜像中的分卷/映像,,#1
    ENVI &&WIMSel=%~1
    ENVI &&VolumeTITLE=+30:分卷%&TAB%180:             名称%&TAB%+60:大小%&TAB%+40:位数%&TAB%180:        显示名称%&TAB%300:  描述
    LABE ,L20T12W370H18,源文件：%&WIMSel%
    TABL VolumeTABL,L20T32W555H350,%&VolumeTITLE%,,0x40
    EDIT+ VolumeEDIT,L50T70W340H16,,,
    ITEM VolumeButton1,L420T398W70H28,确 定,TEAM CALL RealSTATUS3|KILL \,
    ITEM VolumeButton2,L505T398W70H28,关 闭,KILL \,
    ENVI @VolumeTABL.MSG=_%&WM_LBUTTONDOWN%:  CALL VolumePICK    
    TEAM ENVI &&VLSinWIM=| ENVI &&VolumeSel=| ENVI &&K=0    
    ENVI @VolumeInWIM.MSG=#1: CALL WIMMsg1
    TIME WIMTimer3,200, CALL WIMOnTimer3
    TEAM CALL WIMOnTimer3|ENVI &&WIMPATH=%1
    THREAD* GetWIMVolumes %&WIMPATH%
_END

_SUB WIMOnTimer3
    ENVI @VolumeEDIT=正在搜索WIM中的卷，请稍候...  已用时间: %&K%秒
    CALC &K= %&K% + 0.2#1
_END

_SUB CheckUltraISODrv
    IFEX $%&KillVD%=1,EXEC =*ImDisk.exe -D -m %&FFDrv%:
    CALL FreeDrvs
    EXEC =*ImDisk.exe -a -f "%1" -m %&FFDrv%:
_END

_SUB GetWIMVolumes
    TEAM ENVT &&WIMINFO=|ENVI &&vln=|ENVI &&F1=|ENVI &&cPOS1=0|ENVI &&cPOS2=0|ENVI &&Lc=0|ENVI &&cDESC=|ENVI &&HEX_WIMINFO= 
    TEAM ENVI &&Wstr=|ENVI &&DISPOS=0|ENVI &&aSIZE=|ENVI &&aDESC=|ENVI &&bDESC=|ENVI &&szVol=|ENVI &&dDESC=|ENVI &&fDESC= 
    EXEC* -code:UTF8 -exe:*#201  &WIMINFO=!imagex /info %1
    FORX *NL &WIMINFO,&vln,
    {*
        MSTR &F1=<1>%&vln%
        FIND $%&F1%=<IMAGE,
        {
           LPOS &cPOS1=",1,%&vln%
           LPOS &cPOS2=",2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &Wstr=%&cPOS1%,%&Lc%,%&vln%
        }
        LPOS* &DISPOS=<NAME>,1,%&F1%
        IFEX $%&DISPOS% = 1,
        {
           MSTR &cPOS1=11,0,%&vln%        
           MSTR &aDESC=-8,0,%&cPOS1%
        }
        LPOS* &DISPOS=<TOTALBYTES>,1,%&F1%
        IFEX $%&DISPOS% = 1,
        {
           LPOS &cPOS1=>,1,%&vln%
           LPOS &cPOS2=<,2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &aSIZE=%&cPOS1%,%&Lc%,%&vln%
           CALC &aSIZE = %&aSIZE% / 1073741824#2
           IFEX $%&aSIZE% < 0.9, TEAM CALC &aSIZE = %&aSIZE% * 1024#1|ENVI &szVol=[%&aSIZE%MB]! ENVI &szVol=[%&aSIZE%GB]
        }
       LPOS* * &DISPOS=<ARCH>,1,&F1
       IFEX $%&DISPOS% = 1,
        {
           LPOS* * &cPOS1=>,1,&vln
           LPOS* * &cPOS2=<,2,&vln
           CALC #&cPOS1=%&cPOS1%+1
           CALC #&Lc=%&cPOS2%-%&cPOS1%
           MSTR * &dDESC=%&cPOS1%,%&Lc%,&vln
           FIND $%&dDESC%=0,ENVI &cDESC=32位
           FIND $%&dDESC%=9,ENVI &cDESC=64位
        }     
        LPOS* &DISPOS=<DISPLAYNAME>,1,%&F1%
        IFEX $%&DISPOS% = 1,
        {
           LPOS &cPOS1=>,1,%&vln%
           LPOS &cPOS2=<,2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &bDESC=%&cPOS1%,%&Lc%,%&vln%
        }
        LPOS* * &DISPOS=<DESCRIPTION>,1,&F1
        IFEX $%&DISPOS% = 1,
        {
                LPOS* * &cPOS1=>,1,&vln
                LPOS* * &cPOS2=<,2,&vln
                CALC #&cPOS1=%&cPOS1%+1
                CALC #&Lc=%&cPOS2%-%&cPOS1%
                MSTR * &fDESC=%&cPOS1%,%&Lc%,&vln             
        } 
        FIND $%&F1%=</IMAGE>,
        {
            ENVI &VLSinWIM=%&VLSinWIM%%&Wstr%%&TAB%%&aDESC%%&TAB%%&szVol%%&TAB%%&cDESC%%&TAB%%&bDESC%%&TAB%%&fDESC%%&NLDD%              
            TEAM ENVI &Wstr=|ENVI &aSIZE=|ENVI &aDESC=|ENVI &bDESC=|ENVI &szVol=|ENVI &cDESC=|ENVI &dDESC=|ENVI &&fDESC=
        }
    }
    ENVI @WIMTimer3=0
    ENVI @VolumeInWIM.POSTMSG=#1
_END

_SUB WIMMsg1
    TEAM ENVI @WIMTimer3=0| ENVI @VolumeEDIT.Visable=0 
    ENVI @VolumeTABL.Val=1*;%&VLSinWIM% 
    ENVI @VolumeTABL.Sel=1;*
    CALL VolumePICK
_END

_SUB VolumePICK
    ENVI @VolumeTABL.Sel=?&&Sel
    ENVI @VolumeTABL.Val=?%&Sel%.1;&VolumeSel1
    ENVI @VolumeTABL.Val=?%&Sel%.2;&VolumeSel2
    ENVI @VolumeTABL.Val=?%&Sel%.3;&VolumeSel3
    ENVI @VolumeTABL.Val=?%&Sel%.4;&VolumeSel4
    ENVI @VolumeTABL.Val=?%&Sel%.5;&VolumeSel6
    ENVI @VolumeTABL.Val=?%&Sel%.6;&VolumeSel7
    FIND $%&VolumeSel6%=,ENVI &VolumeSel5=%&VolumeSel7%!ENVI &VolumeSel5=%&VolumeSel6%
    ENVI &VolumeSel=%&VolumeSel1% %&VolumeSel2% %&VolumeSel3% %&VolumeSel4% %&VolumeSel5%
_END

_SUB RealSTATUS3
    FIND $%&VolumeSel%=,!
    {
        ENVI. @STATUS3=所选路径/文件：%&WIMSel%-> %&VolumeSel%
    }
_END

_SUB GHOWIMinISO,W600H470,ISO中的镜像列表,,#1
    ENVI &&ISOSel=%~1
    ENVI &&GHOWIMTITLE=150:        映像%&TAB%+30:分卷%&TAB%180:             名称%&TAB%+60:大小%&TAB%+40:位数%&TAB%180:        显示名称%&TAB%300:  描述
    LABE ,L20T12W420H18,源文件：%&ISOSel%
    TABL GHOWIMTABL,L20T32W555H350,%&GHOWIMTITLE%,,0x10040
    EDIT+ GHOWIMEDIT,L50T70W350H16,,,
    ITEM GHOWIMButton1,L420T398W70H28,确 定,TEAM CALL GHOWIMSTATUS3|KILL \,
    ITEM GHOWIMButton2,L505T398W70H28,关 闭,KILL \,
    ENVI @GHOWIMTABL.MSG=_%&WM_LBUTTONDOWN%:  CALL GHOWIMPICK
    ENVI &&GHOWIMSel=
    ENVI &&K=0
    ENVI &&GHOWIMLS=
    ENVI @GHOWIMinISO.MSG=#1: CALL GHOWIMMsg1
    TIME GHOWIMTimer3,200, CALL GHOWIMOnTimer3
    CALL GHOWIMOnTimer3
    ENVI &&ISOPATH=%1
    THREAD* ISO2GHOWIM 
_END

_SUB ISO2GHOWIM
    CALL CheckUltraISODrv %&ISOPATH%
    TEAM ENVI &&aGHOLS=|ENVI &&GLSinISO=|ENVI &&vln=|ENVI &&HD45=
    FORX /S:3 /size:524288000:16106127360 %&FFDrv%:\*.GHO,ANYGHO,0,ENVI &aGHOLS=%&aGHOLS%%&NLDD%%ANYGHO%
    FORX *NL &aGHOLS,&vln,
    {
        FIND $%&vln%=,!
        {
            FNAM &HD45=%&vln%
            FIND $%&HD45%=HD4,! FIND $%&HD45%=HD5,! ENVI &GLSinISO=%&GLSinISO%%&vln%%&NLDD%
        }
    }
    TEAM ENVI &&aWIMLS=|ENVI &&WLSinISO=|ENVI &&R9=
    FORX /S:3 %&FFDrv%:\*.WIM,ANYWIM,0,ENVI &aWIMLS=%&aWIMLS%%&NLDD%%ANYWIM%
    FORX /S:3 %&FFDrv%:\*.ESD,ANYWIM,0,ENVI &aWIMLS=%&aWIMLS%%&NLDD%%ANYWIM%    
    FORX *NL &aWIMLS,&vln,
    {
        FIND $%&vln%=,!
         {
           FNAM &R9=%&vln%
           FIND $%&R9%=BOOT,! CALL GetWIMVolumesInISO "%&vln%"      
         }
    }
    ENVI &GHOWIMLS=%&GLSinISO%%&WLSinISO%
    ENVI &KillVD=1
    ENVI @GHOWIMOnTimer3=0 
    ENVI @GHOWIMinISO.POSTMSG=#1
_END

_SUB GetWIMVolumesInISO
    TEAM ENVT &&WIMINFO=|ENVI &&vln=|ENVI &&F1=|ENVI &&cPOS1=0|ENVI &&cPOS2=0|ENVI &&Lc=0|ENVI &&cDESC=|ENVI &&HEX_WIMINFO=
    TEAM ENVI &&Wstr=|ENVI &&DISPOS=0|ENVI &&aSIZE=|ENVI &&aDESC=|ENVI &&bDESC=|ENVI &&szVol=|ENVI &&dDESC=|ENVI &&fDESC= 
    EXEC* -code:UTF8 -exe:#201 &WIMINFO=!IMAGEX /info %1 
    FORX *NL &WIMINFO,&vln,
    {*
        MSTR &F1=<1>%&vln%
        FIND $%&F1%=<IMAGE,
        {*
           LPOS &cPOS1=",1,%&vln%
           LPOS &cPOS2=",2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &Wstr=%&cPOS1%,%&Lc%,%&vln%
        }
        LPOS* &DISPOS=<NAME>,1,%&F1%
        IFEX $%&DISPOS% = 1,
        {*
           LPOS &cPOS1=>,1,%&vln%
           LPOS &cPOS2=<,2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &aDESC=%&cPOS1%,%&Lc%,%&vln%
        }
        LPOS* &DISPOS=<TOTALBYTES>,1,%&F1%
        IFEX $%&DISPOS% = 1,
        {*
           LPOS &cPOS1=>,1,%&vln%
           LPOS &cPOS2=<,2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &aSIZE=%&cPOS1%,%&Lc%,%&vln%
           CALC &aSIZE = %&aSIZE% / 1073741824#2
           IFEX $%&aSIZE% < 0.9, TEAM CALC &aSIZE = %&aSIZE% * 1024#1|ENVI &szVol=[%&aSIZE%MB]! ENVI &szVol=[%&aSIZE%GB]
        }
        LPOS* * &DISPOS=<ARCH>,1,&F1
        IFEX $%&DISPOS% = 1,
        {*
           LPOS* * &cPOS1=>,1,&vln
           LPOS* * &cPOS2=<,2,&vln
           CALC #&cPOS1=%&cPOS1%+1
           CALC #&Lc=%&cPOS2%-%&cPOS1%
           MSTR * &dDESC=%&cPOS1%,%&Lc%,&vln
           FIND $%&dDESC% = 0,ENVI &cDESC=32位
           FIND $%&dDESC% = 9,ENVI &cDESC=64位
        }     
        LPOS* &DISPOS=<DISPLAYNAME>,1,%&F1%
        IFEX $%&DISPOS% = 1,
        {*
           LPOS &cPOS1=>,1,%&vln%
           LPOS &cPOS2=<,2,%&vln%
           CALC #&cPOS1 = %&cPOS1% + 1
           CALC #&Lc = %&cPOS2% - %&cPOS1%
           MSTR &bDESC=%&cPOS1%,%&Lc%,%&vln%
        }
        LPOS* * &DISPOS=<DESCRIPTION>,1,&F1
        IFEX $%&DISPOS% = 1,
        {*
           LPOS* * &cPOS1=>,1,&vln
           LPOS* * &cPOS2=<,2,&vln
           CALC #&cPOS1=%&cPOS1%+1
           CALC #&Lc=%&cPOS2%-%&cPOS1%
           MSTR * &fDESC=%&cPOS1%,%&Lc%,&vln
        } 
        FIND $%&F1%=</IMAGE>,
        {*
            ENVI &WLSinISO=%&WLSinISO%%~1%&TAB%%&Wstr%%&TAB%%&aDESC%%&TAB%%&szVol%%&TAB%%&cDESC%%&TAB%%&bDESC%%&TAB%%&fDESC%%&NLDD%              
            TEAM ENVI &Wstr=|ENVI &aSIZE=|ENVI &aDESC=|ENVI &bDESC=|ENVI &szVol=|ENVI &cDESC=|ENVI &dDESC=|ENVI &&fDESC=
        }
    }
_END

_SUB GHOWIMOnTimer3
    ENVI @GHOWIMEDIT=正在搜索镜像，请稍候...  已用时间: %&K%秒
    CALC &K= %&K% + 0.2#1
_END

_SUB GHOWIMMsg1
    TEAM ENVI @GHOWIMOnTimer3=0| ENVI @GHOWIMEDIT.Visable=0
    FIND $%&GHOWIMLS%=, TEAM MESS 此ISO前二层目录内搜索不到符合条件的镜像！|KILL \|EXIT _SUB
    ENVI @GHOWIMTABL.Val=1*;%&GHOWIMLS%
    ENVI @GHOWIMTABL.Sel=1;*
    CALL GHOWIMPICK
_END

_SUB GHOWIMPICK 
    ENVI @GHOWIMTABL.Sel=?&&Sel
    ENVI @GHOWIMTABL.Val=?%&Sel%.1;&GHOWIMSel1
    ENVI @GHOWIMTABL.Val=?%&Sel%.2;&GHOWIMSel2
    ENVI @GHOWIMTABL.Val=?%&Sel%.3;&GHOWIMSel3
    ENVI @GHOWIMTABL.Val=?%&Sel%.4;&GHOWIMSel4
    ENVI @GHOWIMTABL.Val=?%&Sel%.5;&GHOWIMSel5
    ENVI @GHOWIMTABL.Val=?%&Sel%.6;&GHOWIMSel7
    ENVI @GHOWIMTABL.Val=?%&Sel%.7;&GHOWIMSel8
    FIND $%&GHOWIMSel7%=,ENVI &GHOWIMSel6=%&GHOWIMSel8%!ENVI &GHOWIMSel6=%&GHOWIMSel7%
    RSTR &&REL10=4,%&GHOWIMSel1%
    FIND $%&REL10%=.GHO,ENVI &GHOWIMSel=%&GHOWIMSel1%!ENVI &GHOWIMSel=%&GHOWIMSel1%-> %&GHOWIMSel2% %&GHOWIMSel3% %&GHOWIMSel4% %&GHOWIMSel5% %&GHOWIMSel6%
_END

_SUB GHOWIMSTATUS3
    FIND $%&GHOWIMSel%=,!
    {
        ENVI. @STATUS3=所选路径/文件：%&GHOWIMSel%
    }
_END

_SUB RESTOREWIM
    IFEX $%&PEPOS% = 0,!! FIND $%&PARTSEL2%=%SYSTEMDRIVE%,!! TEAM MESS 请到PE中还原系统|EXIT _SUB
    ENVI &&szDrv=
    ENVI &SHUTorREBOOT=0
    FDRV &szDrv=%GHOLIST%
    LPOS &&pPOS=：,1,%STATUS3%
    CALC #&pPOS = %&pPOS% + 1
    MSTR &&pFILE=%&pPOS%,0,%STATUS3%
    LPOS* &pPOS=->,1,%&pFILE%
    CALC #&&WIMFILEPOS = %&pPOS% - 1
    LSTR &&WIMFILE=%&WIMFILEPOS%,%&pFILE%
    MSTR &&VolNumString=%&pPOS%,0,%&pFILE%
    MSTR &&VolNum=<2>%&VolNumString%
    RSTR &&IsSWM=4,%&WIMFILE%
    ENVI &&SWMFILE=
    FIND $%&IsSWM%=.SWM, MSTR &SWMFILE=-5,0,%&WIMFILE%
    IFEX %&WIMFILE%,! TEAM MESS. 找不到%&WIMFILE%！|EXIT _SUB
    ENVI @MHGHO2012.Visable=0
    CALL @WIMApplyProgressor
_END

_SUB WIMApplyProgressor,W432H316,WIM还原分区,,#1,,,-discloseb
    LABE. -left ,L26T18W400H31,用"%&WIMFILE%"的第%&VolNum%卷还原到 %&PARTSEL2%,,0xFF0000
    CHEK KillAll,L26T50W380H18,格式化目标分区,,1
    CHEK FixBoot,L26T85W90H18,自动修复引导,,1
    CHEK Unattend,L26T120W90H18,添加无人值守,,0
    LABE -left fghui,L140T123W250H16,适用于原版Win7/8/8.1/10系统,,0xFF0000
    LABE ,L26T157W61H18,完成后：,,
    CHEK WIMAPPLYSHUT,L280T154W62H18,关机,CALL WIMSHUTRB1,0
    CHEK WIMAPPLYRB,L350T154W62H18,重启,CALL WIMSHUTRB2,0
    TEAM ENVI &&p=0|ENVI &&V=|ENVI &&vLn=|ENVI &&L2=
    PBAR PBAR1,L26T186W380H22,0
    LABE -vcenter -trans -ncmd ApplyDoneInfo,L20T213W120H22,,,0xFF0000
    LABE -vcenter -trans -ncmd CalculateInfo,L290T213W120H22,,,0xFF0000
    TEAM ENVI &&TDrvNum=|ENVI &&Tstyle=|ENVI &&EFIDrive=|ENVI &&ActiveDrv=
    TEAM ENVI &&totalSec=0|ENVI &&cSec=0|ENVI &&cMin=0|ENVI &&cHour=0|ENVI &&TMP=0
    TEAM ENVI &&LtoSec=0|ENVI &&LSec=0|ENVI &&LMin=0|ENVI &&LHour=0
    TIME &ApplyTimer,0, CALL OnApplyTimer
    TIME &ElapsedTime,0, CALL CalculateElapsedTime
    ITEM ApplyOK,L226T244W80H28,确 定,CALL OnApply,
    ITEM ApplyCancel,L326T244W80H28,取 消,TEAM ENVI @MHGHO2012.Visable=1|KILL \,
_END

_SUB WIMSHUTRB1
    FIND $%WIMAPPLYSHUT.Check%=1, ENVI @WIMAPPLYRB.Check=0
_END

_SUB WIMSHUTRB2
    FIND $%WIMAPPLYRB.Check%=1, ENVI @WIMAPPLYSHUT.Check=0
_END

_SUB OnApply
    TEAM ENVI @KillAll.Enable=0|ENVI @FixBoot.Enable=0|ENVI @Unattend.Enable=0
    TEAM ENVI @WIMAPPLYSHUT.Enable=0|ENVI @WIMAPPLYRB.Enable=0|ENVI @ApplyOK.Enable=0|ENVI @ApplyCancel.Enable=0 
    IFEX $%KillAll.Check% = 1,
    {
        FIND $%&szDrv%=%&PARTSEL2%,
        {
            MESS. 所选%GHOLIST%在目标分区，无法格式化，请拷贝到其它分区再进行。
            KILL \
            ENVI @MHGHO2012.Visable=1
            KILL @MHGHO2012
            EXIT _SUB
        }
        ENVI @PBAR1=1;正在格式化...
        DFMT %&PARTSEL2%,NTFS, 
        WAIT 1000
    } 
    TEAM ENVI @&ApplyTimer=1000|ENVI @&ElapsedTime=2000
    FIND $%&IsSWM%=.SWM,!
    {
        EXEC*  --cmd::2000:OnApplyMsg -exe:*#201 &V=!IMAGEX.EXE /APPLY "%&WIMFILE%" "%&VolNum%" "%&PARTSEL2%"
    }
    FIND $%&IsSWM%=.SWM,
    {
        EXEC*  --cmd::2000:OnApplyMsg -exe:*#201 &V=!IMAGEX.EXE /ref "%&SWMFILE%*.SWM" /apply "%&WIMFILE%" "%&VolNum%" "%&PARTSEL2%"
    }
    FDIR &&srcWIMDir=%&WIMFILE%
    IFEX %&srcWIMDir%\$OEM$\,
    {
        FILE %&srcWIMDir%\$OEM$\$1\*.*=>%&PARTSEL2%\
        FILE %&srcWIMDir%\$OEM$\$$\*.*=>%&PARTSEL2%\WINDOWS
    }
    ENVI @PBAR1=100;还原成功！
    TEAM ENVI @&ApplyTimer=0|ENVI @&ElapsedTime=0
    TEAM ENVI @ApplyDoneInfo=已用时间：%&cHour%:%&cMin%:%&cSec%|ENVI @CalculateInfo=剩余时间：00:00:00  
    WAIT 2000
    IFEX $%FixBoot.Check% = 1,
    {
      CALL GetTargetPartitionInfo
      CALL AutomaticGuidanceRepair
    }  
    IFEX $%Unattend.Check%=1,CALL Determinedversion
    WAIT 1000
    IFEX $%WIMAPPLYSHUT.Check%=1,ENVI &SHUTorREBOOT=1
    IFEX $%WIMAPPLYRB.Check%=1,ENVI &SHUTorREBOOT=2
    ENVI @MHGHO2012.Visable=1
    KILL @MHGHO2012
    KILL \
_END

_SUB OnApplyMsg
    FIND $%&V%=, EXIT -
    READ -,0,&vLn,%&V%
    MSTR &L2=<2>%&vLn%
    MSTR &p=-2,0,%&L2%
    CALC #&p=%&p%
    IFEX %&p% < 0, EXIT
    ENVI @PBAR1=%&p%;正在还原.....%&p%%%
_END

_SUB OnApplyTimer   
    CALC #&totalSec = %&totalSec% + 1
    CALC #&cSec = %&totalSec% % 60
    CALC #&TMP = %&totalSec% / 60
    CALC #&cMin = %&TMP% % 60
    CALC #&cHour = %&TMP% / 60
    IFEX $%&cSec% < 10, ENVI &cSec=0%&cSec%
    IFEX $%&cMin% < 10, ENVI &cMin=0%&cMin%
    IFEX $%&cHour% < 10, ENVI &cHour=0%&cHour%
    ENVI @ApplyDoneInfo=已用时间：%&cHour%:%&cMin%:%&cSec%
_END

_SUB CalculateElapsedTime
    CALC &LtoSec = ( 100 - %&p% ) / %&p% * %&totalSec%#0 
    CALC #&LSec = %&LtoSec% % 60
    CALC #&TMP = %&LtoSec% / 60
    CALC #&LMin = %&TMP% % 60
    CALC #&LHour = %&TMP% / 60
    IFEX $%&LSec% < 10, ENVI &LSec=0%&LSec%
    IFEX $%&LMin% < 10, ENVI &LMin=0%&LMin%
    IFEX $%&LHour% < 10, ENVI &LHour=0%&LHour%
    ENVI @CalculateInfo=剩余时间：%&LHour%:%&LMin%:%&LSec%
_END

///=========================================================================================================
_SUB AutomaticGuidanceRepair
     FIND $%&Tstyle%=MBR,CALL BootMBR
     FIND $%&Tstyle%=GPT,CALL BootGPT
_END

_SUB BootMBR
    TEAM ENVI &&iVer=|&&VerPOS=|&&ThisVer=
    IFEX %&PARTSEL2%\windows\system32\kernel32.dll,
    {
      SITE ?&iVer=FVER,%&PARTSEL2%\windows\system32\kernel32.dll
      LPOS &VerPOS=.,1,%&iVer%
      CALC #&VerPOS = %&VerPOS% - 1
      LSTR &ThisVer=%&VerPOS%,%&iVer%
      IFEX $%&ThisVer% > 5, TEAM CALL BootNT60|EXIT _SUB
      CALL GetActivePartition
      EXEC -exe:#203 =!bootsect.exe /nt52 %&ActiveDrv%
    }
_END

_SUB BootNT60   
     CALL GetActivePartition
     FIND $%&PARTSEL2%=%&ActiveDrv%,CALL TSELeDrv!CALL ActPART  
_END

_SUB TSELeDrv
     IFEX %&PARTSEL2%\Boot\BCD,!
     {
       EXEC -exe:#202 =!bcdboot.exe %&PARTSEL2%\Windows /s %&ActiveDrv% /f BIOS /l zh-CN
       EXEC -exe:#203 =!bootsect.exe /nt60 %&ActiveDrv% /mbr
     }
     EXEC -exe:#203 =!bootsect.exe /nt60 %&ActiveDrv%    
_END

_SUB ActPART
    IFEX %&ActiveDrv%\Boot\BCD,!
    {
      EXEC -exe:#202 =!bcdboot.exe %&PARTSEL2%\Windows /s %&ActiveDrv% /f BIOS /l zh-CN
      EXEC -exe:#203 =!bootsect.exe /nt60 %&ActiveDrv%
      IFEX %&ActiveDrv%\ntldr,!! IFEX %&ActiveDrv%\boot.ini,!! IFEX %&ActiveDrv%\Windows,!! CALL NT52BCD
      EXIT _SUB
    }
    IFEX %&ActiveDrv%\Boot\BCD,!! IFEX %&ActiveDrv%\BOOTMGR,!! CALL 567HJKI89       
_END

_SUB NT52BCD
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /create {ntldr} /d "Earlier Windows OS Loader"
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set {ntldr} device partition=%&ActiveDrv%
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set {ntldr} path \ntldr
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set {ntldr} description "Windows XP" 
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /displayorder {ntldr} /addlast
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /timeout 5  
    EXEC -exe:#203 =!bootsect.exe /nt60 %&ActiveDrv% /mbr    
_END

_SUB 567HJKI89
    TEAM ENVI &&part=|ENVI &&FORM=|ENVI &&M=1|ENVI &&pou=|ENVI &&A1=|ENVI &&A2=|ENVI &&Lett=1|ENVI &&M1=
    TEAM ENVI &&Lnv=|ENVI &&ID=
    EXEC* -exe:*#204 &part=!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /enum osloader
    READ -,-1,&FORM,%&part%
    LOOP #%&M% <= %&FORM%,
    {
      READ -,%&M%,&pou,%&part% 
      MSTR &A1,&A2=<1><2>%&pou%  
      FIND $%&A1%=device,!! FIND $%&A2%=partition=%&PARTSEL2%,!! TEAM ENVI &Lett=0|ENVI &M1=%&M%|EXIT LOOP
      CALC #&M = %&M% + 1
    }
    IFEX $%&Lett%=0,
    {
      CALC #&M1 = %&M1% - 1
      READ -,%&M1%,&Lnv,%&part%
      MSTR &ID=<2>%&Lnv%
      EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /delete %&ID% /cleanup
      TEAM CALL RTYUUIOFFEFFGGHH|EXIT _SUB
    }
    IFEX $%&Lett%=1,CALL RTYUUIOFFEFFGGHH
_END

 _SUB RTYUUIOFFEFFGGHH 
    TEAM ENVI &&iVer=|ENVI &&part22=|ENVI &&A3=
    HIVE 123,%&PARTSEL2%\Windows\System32\config\SOFTWARE
    REGI HKEY_LOCAL_MACHINE\123\Microsoft\Windows NT\CurrentVersion\ProductName,&iVer
    HIVE 123
    EXEC* -exe:*#204 &part22=!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /create /d "%&iVer%" /application osloader   
    MSTR &A3=<3>,%&part22%
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set %&A3% device  partition=%&PARTSEL2%
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set %&A3% path  \Windows\system32\winload.exe
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set %&A3% locale  zh-CN     
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set %&A3% osdevice  partition=%&PARTSEL2%
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set %&A3% systemroot  \Windows
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /set %&A3% nx   OptIn
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /displayorder %&A3% /addlast 
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /default %&A3%
    EXEC -exe:*#204 =!bcdedit /store "%&ActiveDrv%\BOOT\BCD" /timeout 10
    EXEC -exe:#203 =!bootsect.exe /nt60 %&ActiveDrv%
_END

_SUB BootGPT
    ENVI &&Fexist=0
    CALL SetBOOTAndActive
    FIND $%&EFIDrive%= ,!
    {
      ENVI &Fexist=1
      IFEX %&EFIDrive%\EFI\Boot\BOOTX64.EFI,! ENVI &Fexist=0
      IFEX %&EFIDrive%\EFI\Microsoft\Boot\BCD,! ENVI &Fexist=0
      FIND $%&Fexist%=0,TEAM EXEC -exe:#202 =!bcdboot.exe %&PARTSEL2%\Windows /s %&EFIDrive% /f UEFI /l zh-CN|EXIT _SUB
      FIND $%&Fexist%=1,CALL SetBCDEDIT 
_END

_SUB SetBCDEDIT
    TEAM ENVI &&part=|ENVI &&FORM=|ENVI &&M=1|ENVI &&pou=|ENVI &&A1=|ENVI &&A2=|ENVI &&Lett=1|ENVI &&M1=
    TEAM ENVI &&Lnv=|ENVI &&ID=
    EXEC* -exe:*#204 &part=!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /enum osloader
    READ -,-1,&FORM,%&part%
    LOOP #%&M% <= %&FORM%,
    {
      READ -,%&M%,&pou,%&part% 
      MSTR &A1,&A2=<1><2>%&pou%  
      FIND $%&A1%=device,!! FIND $%&A2%=partition=%&PARTSEL2%,!! TEAM ENVI &Lett=0|ENVI &M1=%&M%|EXIT LOOP
      CALC #&M = %&M% + 1
    }
    IFEX $%&Lett%=0,
    {
      CALC #&M1 = %&M1% - 1
      READ -,%&M1%,&Lnv,%&part%
      MSTR &ID=<2>%&Lnv%
      EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /delete %&ID% /cleanup 
      TEAM CALL RREEWWQQUUII|EXIT _SUB
    }
    IFEX $%&Lett%=1,CALL RREEWWQQUUII
_END

 _SUB RREEWWQQUUII 
    TEAM ENVI &&iVer=|ENVI &&part22=|ENVI &&A3=
    HIVE 123,%&PARTSEL2%\Windows\System32\config\SOFTWARE
    REGI HKEY_LOCAL_MACHINE\123\Microsoft\Windows NT\CurrentVersion\ProductName,&iVer
    HIVE 123
    EXEC* -exe:*#204 &part22=!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /create /d "%&iVer%" /application osloader   
    MSTR &A3=<3>,%&part22%
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /set %&A3% device  partition=%&PARTSEL2%
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /set %&A3% path  \Windows\system32\winload.efi
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /set %&A3% locale  zh-CN     
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /set %&A3% osdevice  partition=%&PARTSEL2%
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /set %&A3% systemroot  \Windows
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /set %&A3% nx   OptIn
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /displayorder %&A3% /addlast 
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /default %&A3%
    EXEC -exe:*#204 =!bcdedit /store "%&EFIDrive%\EFI\Microsoft\Boot\BCD" /timeout 5
_END

//------------判断还原分区所在硬盘分区表是GPT还是MBR
_SUB GetTargetPartitionInfo
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A2=|ENVI &&A8=|ENVI &&tPOS=0
    LPOS &tPOS=:,1,%&PARTSEL1%
    CALC #&tPOS = %&tPOS% - 1
    LSTR &TDrvNum=%&tPOS%,%&PARTSEL1%
    FIND $%&PARTSEL2%=  ,!
    {
        FORX *NL &vFORM,&vLn,
        {
            MSTR* &A2,&A8=<2><8>%&vLn%
            FIND $%&A2%=%&PARTSEL2%,TEAM ENVI &Tstyle=%&A8%|EXIT FORX
        }
        EXIT _SUB
    }
    FIND $%&PARTSEL1%=  ,!
    {
        FORX *NL &vFORM,&vLn,
        {
            MSTR* &A1,&A8=<1><8>%&vLn%
            FIND $%&A1%=%&PARTSEL1%,TEAM ENVI &Tstyle=%&A8%|EXIT FORX
        }
    }
_END

//------------判断mbr分区表下引导盘的盘符
_SUB GetActivePartition
    TEAM ENVI &&vln=|ENVI &&A1=|ENVI &&A2=|ENVI &&A9=|ENVI &&E1=|ENVI &&E2=
    FORX *NL &vFORM,&vln,
    {
        MSTR* &A1,&A2,&A9=<1><2><9>%&vln%
        IFEX $%&A9% = 1,
        {
            LPOS &E1=:,1,%&A1%
            CALC #&E1 = %&E1% - 1
            LSTR &E2=%&E1%,%&A1%
            IFEX $%&E2% = %&TDrvNum%, TEAM ENVI &ActiveDrv=%&A2%|EXIT _SUB
        }
    }
_END

//------------判断gpt分区表下引导盘的盘符
_SUB SetBOOTAndActive
    TEAM ENVI &&vLn=|ENVI &&A1=|ENVI &&A2=|ENVI &&A5=|ENVI &&tPOS=|ENVI &&aNum=|ENVI &&Fexist=0
    FORX *NL &vFORM,&vLn,
    {
        MSTR* &A1,&A2,&A5=<1><2><5>%&vLn%
        FIND $%&A5%=EFI,
        {
            LPOS &tPOS=:,1,%&A1%
            CALC #&tPOS = %&tPOS% - 1
            LSTR &aNum=%&tPOS%,%&A1%
            IFEX $%&aNum% = %&TDrvNum%, TEAM ENVI &EFIDrive=%&A2%|EXIT FORX
        }
    }
_END
//================================================================================================================================
_SUB BACKUPWIM
    IFEX $%&PEPOS% = 0,!! FIND $%&PARTSEL2%=%SYSTEMDRIVE%,!! TEAM MESS 请到PE中备份系统|EXIT _SUB
    TEAM ENVI &&pBLK=|ENVI &&szDrive=|ENVI &&szDrvPOS=0
    MSTR &pBLK=<1->%GHOBACK%
    LPOS &szDrvPOS=\,1,%&pBLK%
    IFEX $%&szDrvPOS% = 0, TEAM MESS 请选择合法的保存路径。|EXIT _SUB
    CALC #&szDrvPOS = %&szDrvPOS% - 1
    LSTR &szDrive=%&szDrvPOS%,%&pBLK%
    TEAM ENVI &&legalDrv=|ENVI &&legalNum=
    CALL CheckBKPathLegal "%&szDrive%"
    FIND $%&legalDrv%=,!! FIND $%&legalNum%=,!! TEAM MESS 备份的保存路径不合法，请重新指定。|EXIT _SUB
    RPOS &&pDIR=\,1,%&pBLK%
    LSTR &&pMKDIR=%&pDIR%,%&pBLK%
    ENVI &&ExistFolder=0
    IFEX %&pMKDIR%, ENVI &ExistFolder=1!MDIR %&pMKDIR%
    ENVI @MHGHO2012.Visable=0
    IFEX %&pBLK%, CALL @WIMAppend! CALL @WIMCapture
_END

_SUB WIMCapture,W432H315,WIM备份分区,,#1,,,-discloseb
    LABE. -left ,L26T16W400H31,把 %&PARTSEL2% 备份到"%&pBLK%",,0xFF0000
    LABE ,L26T50W80H16,名称：,
    EDIT WIMName,L108T48W280H18,,
    LABE ,L26T80W80H16,描述：,    
    date *space &&szTime1
    MSTR &&B1,&&B2,&&B3,&&B5,&&B6,&&B7=<1><2><3><5><6><7>%&szTime1% 
    EDIT WIMDescribe,L108T78W280H19,%&B1%-%&B2%-%&B3% %&B5%:%&B6%:%&B7%,
    LABE ,L26T113W80H16,压缩级别：,
    LIST WIMCompress,L108T109W90H20,最大压缩|快速压缩|不压缩,,最大压缩,
    LABE ,L26T150W61H18,完成后：,,
    CHEK WIMCaptureSHUT,L88T147W62H18,关机,CALL CaptureSHUTRB1,0
    CHEK WIMCaptureRB,L152T147W62H18,重启,CALL CaptureSHUTRB2,0
    TEAM ENVI &&p=0|ENVI &&V=|ENVI &&vLn=|ENVI &&L2=
    PBAR CaptureBar,L26T185W380H22,0
    LABE -center -vcenter -trans -ncmd CaptureDoneInfo,L25T208W381H18,,,0xFF0000
    TEAM ENVI &&totalSec=0|ENVI &&cSec=0|ENVI &&cMin=0|ENVI &&cHour=0|ENVI &&TMP=0
    TIME &CaptureTimer,0, CALL OnCaptureTimer
    ITEM CaptureOK,L226T240W80H28,确 定,CALL OnCapture,
    ITEM CaptureCancel,L326T240W80H28,取 消,TEAM ENVI @MHGHO2012.Visable=1|KILL \,  
_END

_SUB CaptureSHUTRB1
    FIND $%WIMCaptureSHUT.Check%=1, ENVI @WIMCaptureRB.Check=0
_END

_SUB CaptureSHUTRB2
    FIND $%WIMCaptureRB.Check%=1, ENVI @WIMCaptureSHUT.Check=0
_END

_SUB OnCapture
    TEAM ENVI @CaptureOK.Enable=0|ENVI @WIMName.Enable=0|ENVI @WIMDescribe.Enable=0|ENVI @WIMCompress.Enable=0
    TEAM ENVI @CaptureCancel.Enable=0|ENVI @WIMCaptureRB.Enable=0|ENVI @WIMCaptureSHUT.Enable=0
    ENVI &&CMPR=
    FIND $%WIMCompress%=快速压缩,ENVI &CMPR=/compress fast
    FIND $%WIMCompress%=最大压缩,ENVI &CMPR=/compress maximum
    FIND $%WIMCompress%=不压缩,ENVI &CMPR=/compress none
    SET &p=-1
    ENVI @CaptureDoneInfo=已用时间：00:00:00
    ENVI @&CaptureTimer=1000
    EXEC*  --cmd::2000:OnCaptureMsg -exe:#201  &V=!IMAGEX.EXE /capture "%&PARTSEL2%" "%&pBLK%" "%WIMName%" "%WIMDescribe%" %&CMPR%
    ENVI @&CaptureTimer=0
    ENVI &&NewWIMSize=0
    IFEX %&pBLK%, SIZE &NewWIMSize=%&pBLK%
    IFEX $%&NewWIMSize% = 0, ENVI @CaptureBar=100;备份失败！! ENVI @CaptureBar=100;备份成功！
    WAIT 3000
    FIND $%HideFolder.Check%=1, IFEX %&pMKDIR%, SITE %&pMKDIR%,+H
    IFEX $%WIMCaptureSHUT.Check% = 1, ENVI &SHUTorREBOOT=1
    IFEX $%WIMCaptureRB.Check% = 1, ENVI &SHUTorREBOOT=2
    ENVI @MHGHO2012.Visable=1
    KILL @MHGHO2012
    KILL \
_END

_SUB OnCaptureMsg
    FIND $%&V%=, EXIT -
    SET &p0=%&p%
    READ -,0,&vLn,%&V%
    MSTR &L2=<2>%&vLn%
    MSTR &p=-2,0,%&L2%
    CALC #&p=%&p%
    IFEX %&p% < 0, EXIT
    IFEX $%&p% = %&p0%, EXIT
    ENVI @CaptureBar=%&p%;正在备份.....%&p%%%
_END

_SUB OnCaptureTimer
    CALC #&totalSec = %&totalSec% + 1
    CALC #&cSec = %&totalSec% % 60
    CALC #&TMP = %&totalSec% / 60
    CALC #&cMin = %&TMP% % 60
    CALC #&cHour = %&TMP% / 60
    IFEX $%&cSec% < 10, ENVI &cSec=0%&cSec%
    IFEX $%&cMin% < 10, ENVI &cMin=0%&cMin%
    IFEX $%&cHour% < 10, ENVI &cHour=0%&cHour%
    ENVI @CaptureDoneInfo=已用时间：%&cHour%:%&cMin%:%&cSec%
_END

_SUB WIMAppend,W432H332,增量/覆盖备份,,#1,,,-discloseb
    LABE. -left ,L26T16W400H31,把 %&PARTSEL2% 备份到"%&pBLK%",,0xFF0000
    LABE ,L26T51W50H16,名称：,
    EDIT AppendName,L78T48W320H18,
    LABE ,L26T81W50H16,描述：
    date *space &&szTime
    MSTR &&A1,&&A2,&&A3,&&A5,&&A6,&&A7=<1><2><3><5><6><7>%&szTime%
    EDIT Appendmiaos,L78T78W320H18,%&A1%-%&A2%-%&A3% %&A5%:%&A6%:%&A7%,
    GROU ,L26T104W188H94
    RADI SelectIncrement,L38T119W160H18,增量备份,CALL EnableCompress,1
    RADI SelectCapture,L38T144W160H18,覆盖原有备份,CALL EnableCompress,0
    LABE -right DescCompress,L35T170W80H16,压缩级别：,
    ENVI @DescCompress.Enable=0
    LIST SelectCompress,L116T166W90H20,最大压缩|快速压缩|不压缩,,最大压缩,-
    GROU ,L230T104W172H94
    LABE ,L245T119W100H18,完成后：,,
    CHEK WIMAppendSHUT,L270T140W100H18,关机,CALL AppendSHUTRB1,0
    CHEK WIMAppendRB,L270T166W100H18,重启,CALL AppendSHUTRB2,0
    TEAM ENVI &&p=0|ENVI &&V=|ENVI &&vLn=|ENVI &&L2=
    PBAR AppendBar,L26T212W380H22,0
    LABE -center -vcenter -trans -ncmd AppendDoneInfo,L25T234W381H18,,,0xFF0000
    TEAM ENVI &&totalSec=0|ENVI &&cSec=0|ENVI &&cMin=0|ENVI &&cHour=0|ENVI &&TMP=0
    TIME &AppendTimer,0, CALL OnAppendTimer
    ITEM AppendOK,L226T260W80H28,确 定,CALL CaptureOrAppend,
    ITEM AppendCancel,L326T260W80H28,取 消,TEAM ENVI @MHGHO2012.Visable=1|KILL \,    
_END

_SUB AppendSHUTRB1
    FIND $%WIMAppendSHUT.Check%=1, ENVI @WIMAppendRB.Check=0
_END

_SUB AppendSHUTRB2
    FIND $%WIMAppendRB.Check%=1, ENVI @WIMAppendSHUT.Check=0
_END

_SUB EnableCompress
    FIND $%SelectIncrement.Check%=1, TEAM ENVI @DescCompress.Enable=0|ENVI @SelectCompress.Enable=0|EXIT _SUB
    FIND $%SelectCapture.Check%=1, TEAM ENVI @DescCompress.Enable=1|ENVI @SelectCompress.Enable=1
_END

_SUB CaptureOrAppend
    FIND $%SelectIncrement.Check%=1, TEAM CALL OnAppend|EXIT _SUB
    CALL StillCaptureWIM
_END

_SUB OnAppend
    TEAM ENVI @AppendName.Enable=0|ENVI @Appendmiaos.Enable=0|ENVI @SelectIncrement.Enable=0|ENVI @SelectCapture.Enable=0 
    TEAM ENVI @SelectCompress.Enable=0|ENVI @WIMAppendSHUT.Enable=0|ENVI @WIMAppendRB.Enable=0|ENVI @AppendOK.Enable=0|ENVI @AppendCancel.Enable=0
    TEAM ENVI &&iTIME=|ENVI &&T1=|ENVI &&T2=|ENVI &&T3=|ENVI &&T4=|ENVI &&T5=|ENVI &&T6=|ENVI &&T7=|ENVI &&OldWIMTime=
    IFEX %&pBLK%,
    {
        SITE ?-local ,&iTIME=FTIME,%&pBLK%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &OldWIMTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    SET &p=-1
    ENVI @AppendDoneInfo=已用时间：00:00:00
    ENVI @&AppendTimer=1000
    EXEC*  --cmd::2000:OnAppendMsg -exe:#201 &V=!IMAGEX.EXE /append "%&PARTSEL2%" "%&pBLK%" "%AppendName%" "Appendmiaos"
    ENVI @&AppendTimer=0
    TEAM ENVI &&NewWIMSize=0|ENVI &&NewWIMTime=|ENVI &&WIMFailure=0
    IFEX %&pBLK%,
    {
        SIZE &NewWIMSize=%&pBLK%
        SITE ?-local ,&iTIME=FTIME,%&pBLK%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &NewWIMTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    FIND $%&NewWIMTime%=%&OldWIMTime%, ENVI &WIMFailure=1
    IFEX $%&NewWIMSize% = 0, ENVI &WIMFailure=1
    IFEX $%&WIMFailure% = 0, ENVI @AppendBar=100;增量备份成功！! ENVI @AppendBar=100;增量备份失败！
    WAIT 3000
    FIND $%HideFolder.Check%=1, IFEX %&pMKDIR%, SITE %&pMKDIR%,+H
    IFEX $%WIMAppendSHUT.Check% = 1, ENVI &SHUTorREBOOT=1
    IFEX $%WIMAppendRB.Check% = 1, ENVI &SHUTorREBOOT=2
    ENVI @MHGHO2012.Visable=1
    KILL @MHGHO2012
    KILL \
_END

_SUB OnAppendMsg
    FIND $%&V%=, EXIT -
    SET &p0=%&p%
    READ -,0,&vLn,%&V%
    MSTR &L2=<2>%&vLn%
    MSTR &p=-2,0,%&L2%
    CALC #&p=%&p%
    IFEX %&p% < 0, EXIT
    IFEX $%&p% = %&p0%, EXIT
    ENVI @AppendBar=%&p%;正在备份.....%&p%%%
_END

_SUB OnAppendTimer
    CALC #&totalSec = %&totalSec% + 1
    CALC #&cSec = %&totalSec% % 60
    CALC #&TMP = %&totalSec% / 60
    CALC #&cMin = %&TMP% % 60
    CALC #&cHour = %&TMP% / 60
    IFEX $%&cSec% < 10, ENVI &cSec=0%&cSec%
    IFEX $%&cMin% < 10, ENVI &cMin=0%&cMin%
    IFEX $%&cHour% < 10, ENVI &cHour=0%&cHour%
    ENVI @AppendDoneInfo=已用时间：%&cHour%:%&cMin%:%&cSec%
_END

_SUB StillCaptureWIM
    TEAM ENVI @AppendName.Enable=0|ENVI @Appendmiaos.Enable=0|ENVI @SelectIncrement.Enable=0|ENVI @SelectCapture.Enable=0 
    TEAM ENVI @SelectCompress.Enable=0|ENVI @WIMAppendSHUT.Enable=0|ENVI @WIMAppendRB.Enable=0|ENVI @AppendOK.Enable=0|ENVI @AppendCancel.Enable=0 
    ENVI &&CMPR=
    FIND $%SelectCompress%=快速压缩,ENVI &CMPR=/compress fast
    FIND $%SelectCompress%=最大压缩,ENVI &CMPR=/compress maximum
    FIND $%SelectCompress%=不压缩,ENVI &CMPR=/compress none
    TEAM ENVI &&iTIME=|ENVI &&T1=|ENVI &&T2=|ENVI &&T3=|ENVI &&T4=|ENVI &&T5=|ENVI &&T6=|ENVI &&T7=|ENVI &&OldWIMTime=
    IFEX %&pBLK%,
    {
        SITE ?-local ,&iTIME=FTIME,%&pBLK%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &OldWIMTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    SET &p=-1
    ENVI @AppendDoneInfo=已用时间：00:00:00
    ENVI @&AppendTimer=1000
    EXEC*  --cmd::2000:OnAppendMsg -exe:#201 &V=!IMAGEX.EXE /capture "%&PARTSEL2%" "%&pBLK%" "%AppendName%" "Appendmiaos" %&CMPR%
    ENVI @&AppendTimer=0
    TEAM ENVI &&NewWIMSize=0|ENVI &&NewWIMTime=|ENVI &&WIMFailure=0
    IFEX %&pBLK%,
    {
        SIZE &NewWIMSize=%&pBLK%
        SITE ?-local ,&iTIME=FTIME,%&pBLK%
        MSTR &T1,&T2,&T3,&T4,&T5,&T6,&T7=<1><2><3><4><5><6><7>%&iTIME%
        ENVI &NewWIMTime=%&T1%%&T2%%&T3%%&T4%%&T5%%&T6%%&T7%
    }
    FIND $%&NewWIMTime%=%&OldWIMTime%, ENVI &WIMFailure=1
    IFEX $%&NewWIMSize% = 0, ENVI &WIMFailure=1
    IFEX $%&WIMFailure% = 0, ENVI @AppendBar=100;覆盖备份成功！! ENVI @AppendBar=100;覆盖备份失败！
    WAIT 3000
    FIND $%HideFolder.Check%=1, IFEX %&pMKDIR%, SITE %&pMKDIR%,+H
    IFEX $%WIMAppendSHUT.Check% = 1, ENVI &SHUTorREBOOT=1
    IFEX $%WIMAppendRB.Check% = 1, ENVI &SHUTorREBOOT=2
    ENVI @MHGHO2012.Visable=1
    KILL @MHGHO2012
    KILL \
_END

///-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_SUB Determinedversion
   TEAM ENVI &&Shuzhi=|ENVI &&iVer=
   HIVE 123,%&PARTSEL2%\Windows\System32\config\SOFTWARE
   REGI HKEY_LOCAL_MACHINE\123\Microsoft\Windows NT\CurrentVersion\ProductName,&iVer
   MSTR &Shuzhi=<2>%&iVer%
   HIVE 123
   IFEX %&PARTSEL2%\Windows\SysWOW64,ENVI &Systemdigits=amd64!ENVI &Systemdigits=x86
   IFEX %&PARTSEL2%\Windows\Panther\Unattend.xml,!
     {
       MDIR %&PARTSEL2%\Windows\Panther
       FIND $%&Shuzhi%=7,CALL WINDOWS7
       FIND $%&Shuzhi%=10,CALL WINDOWSyui10
       FIND $%&Shuzhi%=8,CALL WINDOWS8
       FIND $%&Shuzhi%=8.1,CALL WINDOWS8.1
     }   
_END

_SUB WINDOWS7
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<?xml version="1.0" encoding="utf-8"?>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<unattend xmlns="urn:schemas-microsoft-com:unattend">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<settings pass="oobeSystem">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<component name="Microsoft-Windows-Shell-Setup" processorArchitecture="%&Systemdigits%" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<OOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipMachineOOBE>true</SkipMachineOOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</OOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<TimeZone>China Standand Time</TimeZone>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<AutoLogon>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Password>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Value>UABhAHMAcwB3AG8AcgBkAA==</Value>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<PlainText>false</PlainText>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</Password>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Username>Administrator</Username>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Enabled>true</Enabled> 
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</AutoLogon>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</component>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</settings>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</unattend>
_END

_SUB WINDOWS8
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<?xml version="1.0" encoding="utf-8"?>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<unattend xmlns="urn:schemas-microsoft-com:unattend">
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<settings pass="oobeSystem">
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<component name="Microsoft-Windows-Shell-Setup" processorArchitecture="%&Systemdigits%" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<OOBE>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipMachineOOBE>true</SkipMachineOOBE>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipUserOOBE>false</SkipUserOOBE>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</OOBE>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<AutoLogon>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Username>Administrator</Username>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Enabled>true</Enabled>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<LogonCount>1</LogonCount>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</AutoLogon>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</component>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</settings>
   WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</unattend>   
_END


_SUB WINDOWS8.1
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<?xml version="1.0" encoding="utf-8"?>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<unattend xmlns="urn:schemas-microsoft-com:unattend">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<settings pass="oobeSystem">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<component name="Microsoft-Windows-Shell-Setup" processorArchitecture="%&Systemdigits%" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<OOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipMachineOOBE>true</SkipMachineOOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipUserOOBE>false</SkipUserOOBE> 
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</OOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<UserAccounts>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<LocalAccounts>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<LocalAccount wcm:action="add">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Password>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Value>UABhAHMAcwB3AG8AcgBkAA==</Value>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<PlainText>false</PlainText>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</Password>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Group>Administrators</Group>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Name>MyPC</Name>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</LocalAccount>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</LocalAccounts>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</UserAccounts>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</component>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</settings>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</unattend>
_END

_SUB WINDOWSyui10
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<?xml version="1.0" encoding="utf-8"?>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<unattend xmlns="urn:schemas-microsoft-com:unattend">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<settings pass="oobeSystem">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<component name="Microsoft-Windows-Shell-Setup" processorArchitecture="%&Systemdigits%" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<OOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipMachineOOBE>true</SkipMachineOOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<SkipUserOOBE>false</SkipUserOOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</OOBE>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<AutoLogon>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Username>Administrator</Username>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Enabled>true</Enabled>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<LogonCount>1</LogonCount>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</AutoLogon>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<LogonCommands>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<AsynchronousCommand wcm:action="add">
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<CommandLine>%WINDIR%\1.cmd</CommandLine>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Description>Active</Description>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,<Order>1</Order>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</AsynchronousCommand>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</LogonCommands> 
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</component> 
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</settings>
    WRIT "%&PARTSEL2%\Windows\Panther\Unattend.xml",$+0,</unattend>
_END
