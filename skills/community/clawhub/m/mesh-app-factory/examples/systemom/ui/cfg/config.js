export default {
inject:['service', 'tags'],
data() {return {
company:{
    cid:'',
    creditCode:"",
    name:"",
    location:{province:'',city:'',county:''},
    accessCode:"",
    logLevel:'DEBUG',
    tokenPwd:"",
    runMode:'SINGLETON',
    logo:"/assets/imgs/logo_example.png"
},
cmds:{setloglevel:false,setoutsideaddr:false,resettokenpwd:false},
outsideAddr:'', //为空时，表示不开启
addrList:[],
chgPwdDta:{oldPwd:'',newPwd:'',cfmPwd:'',vis:false,dlg:false},
logoOpts:{
    img: "/assets/imgs/logo_example.png",
    size: 1,
    full: false,
    outputType: "png",
    canMove: true,
    fixedBox: true,
    original: false,
    canMoveBox: true,
    autoCrop: true,
    // 只有自动截图开启 宽度高度才生效
    autoCropWidth: 150,
    autoCropHeight: 150,
    centerBox: false,
    high: false,
    cropData: {},
    enlarge: 1,
    mode: 'contain',
    maxImgSize: 3000,
    limitMinSize: [50, 50],
    fixed: true,
    fixedNumber: [1, 1],
    
    dlg:false,
    width:'60vw',
    loading:false
},
logLevels:['DEBUG','INFO','WARN','ERROR']
}},
created(){
    var w=document.documentElement.clientWidth;
    var h=document.documentElement.clientHeight;
    if(w>h) {
        this.logoOpts.width=parseInt(h*0.6);
    }else{
        this.logoOpts.width=parseInt(w*0.6);
    }
    this.init();
    this.service.supportedCmds().then(list=> {
        this.cmds.setloglevel=findInArray(list,'setloglevel')>=0;
        this.cmds.setoutsideaddr=findInArray(list,'setoutsideaddr')>=0;
        this.cmds.resettokenpwd=findInArray(list,'resettokenpwd')>=0;
    });
},
methods:{
init() {
    var dta = {cmd:"query"};
    this.cid=Companies.curCompanyId();
    this.service.command(dta).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var info=resp.data;
        if(this.cid != info.companyId) {
            this.$refs.alertDlg.show(this.tags.cfg.invalidCid);
            return;
        }
        this.company.accessCode=info.accessCode;
        this.company.name=info.companyName;
        this.company.creditCode=info.creditCode;
        this.company.location={province:info.province,city:info.city,county:info.county};
        this.logLevel=info.logLevel;
        this.outsideAddr=info.outsideAddr;
        
        var l=[];
        if(info.mode) {
            this.runMode=info.mode;
            if(info.mode!='ROOT') {
                for(var addr of info.externAddrs) {
                    l.push({label:addr, value:addr})
                }
                l.push({label:this.tags.dontSet, value:""});
            }
        }
        this.addrList=l;
        Companies.getLogo(this.cid, __regsiterCallback(png=> {
            if(png) {
                this.company.logo=png;
            }
        }));
    });
},
resetAccessCode() { //用于重置httpdns服务接入码
    this.service.command({cmd:"resetAccessCode"}).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        } else {
            this.company.accessCode=resp.data.code;
        }
    });
},
saveAccessCode(val, initVal) { //用于保存httpdns服务接入码
    this.service.command({cmd:"saveAccessCode", code:val}).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        } else {
            this.company.accessCode=val;
        }
    });
},
resetTokenPwd(){//用于重置公司调测服务的令牌
    this.service.command({cmd:"resettokenpwd"}).then(resp=>{
        if(resp.code==RetCode.OK) {
            this.company.tokenPwd=resp.data.token;
        }
    });
},
selectImg() {
  this.$refs.logoImg.dispatchEvent(new MouseEvent('click'))
},
startCropLogo(e) {
  this.logoOpts.loading=true;
  this.$refs.cropper.startCrop();
  //选择图片
  var file = e.target.files[0];
  if (!/\.(gif|jpg|jpeg|png|bmp|GIF|JPG|PNG)$/.test(e.target.value)) {
    this.$refs.alertDlg.show(this.tags.invalidImg);
    return false;
  }
  var reader = new FileReader()
  reader.onload = (e) => {
    var data
    if (typeof e.target.result === 'object') {
      // 把Array Buffer转化为blob 如果是base64不需要
      data = window.URL.createObjectURL(new Blob([e.target.result]))
    } else {
      data = e.target.result
    }
    this.logoOpts.img = data
    this.logoOpts.loading=false;
  }
  // reader.readAsDataURL(file)// 转化为base64
  reader.readAsArrayBuffer(file)// 转化为blob
},
zoom(in_out) {
  this.$refs.cropper.changeScale(in_out)
},
rotate(dir) {
  if(dir==1) {
    this.$refs.cropper.rotateLeft();
  } else {
    this.$refs.cropper.rotateRight();
  }
},
setLogo() {
  this.$refs.cropper.getCropData(logo => {
    this.company.logo=logo;
    this.service.request_cloud({method:"PUT",url:"/company/setLogo",data:{logo:logo}},"company").then(resp=>{
      if(resp.code!=RetCode.OK) {
        this.$refs.alertDlg.showErr(resp.code, resp.info);
        return;
      }
      Companies.saveLogo(this.cid, logo);
      this.logoOpts.dlg=false;
      this.$refs.cropper.stopCrop()
    });
  })
},
outsideAddrAdded(val, initVal) {
    if(!Http.isIPv4(val) && !Http.isIPv6(val)) {
        return;
    }
    //自有公网IP的情况，需要设置外网地址
    if(Http.isLanIP(val)) {
        this.$refs.alertDlg.show(val + this.tags.invalidExtIP);
        return;
    }
    this.service.command({addr:val,cmd:"setOutsideAddr"}).then(resp => {
      if(resp.code==RetCode.OK) {
        this.addrList.push({label:val,value:val});
        this.outsideAddr=val;
      } 
    });
},
outsideAddrChged() {
    this.service.command({addr:this.outsideAddr,cmd:"setOutsideAddr"})
},
logLevelChged() {
    this.service.command({level:this.company.logLevel,cmd:"setLogLevel"})
},
addrChged() {
    this.service.command({cmd:"setInfo",
        province:this.company.location.province,
        city:this.company.location.city,
        county:this.company.location.county
    });
},
nameChged() {
    this.service.command({cmd:"setInfo", name:this.company.name});
},
connectionTest() {
    var addr;
    if(Http.isIPv6(this.outsideAddr)) {
        addr='['+this.outsideAddr+']:8523';
    } else {
        addr=this.outsideAddr+':8523';
    }
            
    this.$refs.procDlg.show(this.tags.cfg.outsideTest,
        this.tags.cfg.outTestDesc, 'leak_add',
        (dlg)=> {
            dlg.setInfo(this.tags.doing);
            var opts={method:"GET",url:"/api/test?addr="+addr,cloud:true};
            return request(opts, "httpdns");            
        },
        (dlg,resp)=> {
          if(resp.code!=RetCode.OK) {
            dlg.setInfo(this.tags.failToConnect + addr);
          } else {
            dlg.setInfo(this.tags.succeedToConnect + addr);
          }
        }
    )
},
changePwd() {
    this.service.command({oldPwd:this.chgPwdDta.oldPwd,
        newPwd:this.chgPwdDta.newPwd,
        cfmPwd:this.chgPwdDta.cfmPwd,
        cmd:"changePwd"}).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        } else {
            this.chgPwdDta={oldPwd:'',newPwd:'',cfmPwd:'',vis:false,dlg:false};
            this.$refs.alertDlg.show(this.tags.successToChgPwd);
        }
    });
}
},
template: `
<q-layout view="hHh lpr fFf">
<q-header class="bg-grey-1 text-primary">
   <q-toolbar>
      <q-btn flat icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{tags.cfg.title}}</q-toolbar-title>
   </q-toolbar>
</q-header>
<q-page-container>
 <q-page>
<q-markup-table bordered="false" flat>
 <tr class="q-mb-sm text-dark bg-blue-grey-1">
  <td class="text-bold">{{tags.cfg.baseSettings}}</td>
  <td align="right" @click="chgPwdDta.dlg=true">{{tags.chgPwd}}</td>
 </tr>
 <tr>
   <td>{{tags.cfg.id}}</td>
   <td>{{cid}}</td>
 </tr>
 <tr>
   <td>{{tags.cfg.creditCode}}</td>
   <td>{{company.creditCode}}</td>
 </tr>
 <tr>
   <td>{{tags.cfg.name}}</td>
   <td class="cursor-pointer">{{company.name}}
    <q-popup-edit v-model="company.name" v-slot="scope" @update:model-value="nameChged"
     buttons :label-set="tags.ok" :label-cancel="tags.cancel" auto-save>
     <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set"></q-input>
    </q-popup-edit>
   </td>
 </tr>
 <tr>
   <td>{{tags.cfg.address}}</td>
   <td class="cursor-pointer">
    <address-input v-model="company.location"
     @update:model-value="addrChged"></address-input>
   </td>
 </tr>
 <tr>
  <td>{{tags.cfg.logo}}</td>
  <td>
   <q-img :src="company.logo" style="width:5em;height:5em;" @click="logoOpts.dlg=true"></q-img>
  </td>
 </tr>
 <tr>
   <td>{{tags.cfg.backup}}</td>
   <td @click="service.go_to('/cfg/backup')">
    <q-icon name="cloud_sync" color="primary" size="2em" class="q-ml-md"></q-icon>
   </td>
 </tr>
 <tr class="q-mb-sm text-dark bg-blue-grey-1 text-bold">
  <td>{{tags.cfg.nwSettings}}
   <q-btn round dense flat icon="leak_add" class="q-ml-sm"
    @click="connectionTest" color="secondary"></q-btn>
  </td>
  <td align="right">
   <q-btn round dense flat icon="add_circle" color="primary">
    <q-popup-edit v-slot="scope" @save="outsideAddrAdded"
     buttons :label-set="tags.ok" :label-cancel="tags.cancel" auto-save>
     <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set"></q-input>
    </q-popup-edit>
   </q-btn>
  </td>
 </tr>
 <tr>
   <td>{{tags.cfg.accessCode}}</td>
   <td><span>{{company.accessCode}}
    <q-popup-edit v-slot="scope" @save="saveAccessCode" v-model="company.accessCode"
     buttons :label-set="tags.ok" :label-cancel="tags.cancel" auto-save>
     <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set"></q-input>
    </q-popup-edit>
    </span>
    <q-btn round dense flat icon="auto_mode" text-color="secondary"
    @click="resetAccessCode" class="q-ml-md"></q-btn>
   </td>
 </tr>
 <tr v-if="cmds.setoutsideaddr">
  <td>{{tags.cfg.pubGwIp}}</td>
  <td>
   <q-select v-model="outsideAddr" :options="addrList" emit-value
    @update:model-value="outsideAddrChged" dense></q-select>
  </td>
 </tr>
 <tr class="q-mb-sm text-dark bg-blue-grey-1 text-bold"
  v-if="cmds.resettokenpwd||cmds.setloglevel">
  <td>{{tags.cfg.remoteTest}}</td><td></td>
 </tr>
 <tr v-if="cmds.resettokenpwd">
   <td>{{tags.cfg.tokenPwd}}<q-icon name="key"></q-icon></td>
   <td>{{company.tokenPwd}}
      <q-icon name="refresh" class="q-ml-md" color="primary" @click="resetTokenPwd" size="1.5em"></q-icon>
   </td>
 </tr>
 <tr v-if="cmds.setloglevel">
   <td>{{tags.cfg.logLevel}}</td>
   <td>
    <q-select v-model="company.logLevel" :options="logLevels"
     @update:model-value="logLevelChged" dense></q-select>
   </td>
 </tr>
</q-markup-table>

 </q-page>
</q-page-container>
</q-layout>

<q-dialog v-model="logoOpts.dlg">
 <q-card bordered>
   <q-card-section>
    <div class="row no-wrap">
     <div>
      <!-- logoOpts必须用v-bind不能用v-model -->
      <vue-cropper ref="cropper" v-bind="logoOpts"
       :style="{width:logoOpts.width+'px',height:logoOpts.width+'px'}">
      </vue-cropper>
     </div>
     <div class="column items-start">
        <q-btn flat icon="burst_mode" color="primary" @click="selectImg" size="1.4em"></q-btn>
        <q-btn flat icon="zoom_in" color="accent" @click="zoom(1)" size="1.2em"></q-btn>
        <q-btn flat icon="zoom_out" color="accent" @click="zoom(-1)" size="1.2em"></q-btn>
        <q-btn flat icon="rotate_left" color="accent" @click="rotate(1)" size="1.2em"></q-btn>
        <q-btn flat icon="rotate_right" color="accent" @click="rotate(-1)" size="1.2em"></q-btn>
     </div>
    </div>
   </q-card-section>
   <q-inner-loading :showing="logoOpts.loading"><q-spinner-gears size="4em" color="primary"></q-spinner-gears></q-inner-loading>
   <q-card-actions align="right" class="text-primary">
    <q-btn flat :label="tags.ok" @click="setLogo"></q-btn>
    <q-btn flat :label="tags.cancel" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
 <input type="file" ref="logoImg" v-show="false"
   style="position:absolute;clip:rect(0 0 0 0);"
   accept="image/png, image/jpeg, image/gif, image/jpg"
   @change="startCropLogo($event)">
</q-dialog>

<q-dialog v-model="chgPwdDta.dlg">
 <q-card bordered>
   <q-card-section>
    <q-input v-model="chgPwdDta.oldPwd" :label="tags.oldPwd" dense :type="chgPwdDta.vis ? 'text':'password'">
     <template v-slot:append>
      <q-icon :name="chgPwdDta.vis ? 'visibility':'visibility_off'"
        class="cursor-pointer" @click="chgPwdDta.vis=!chgPwdDta.vis"></q-icon>
     </template>
    </q-input>
    <q-input v-model="chgPwdDta.newPwd" :label="tags.newPwd" dense :type="chgPwdDta.vis ? 'text':'password'">
     <template v-slot:append>
      <q-icon :name="chgPwdDta.vis ? 'visibility':'visibility_off'"
        class="cursor-pointer" @click="chgPwdDta.vis=!chgPwdDta.vis"></q-icon>
     </template>
    </q-input>
    <q-input v-model="chgPwdDta.cfmPwd" :label="tags.cfmPwd" dense :type="chgPwdDta.vis ? 'text':'password'"
     :rules="[v=>chgPwdDta.newPwd==chgPwdDta.cfmPwd||tags.invalidCfmPwd]">
     <template v-slot:append>
      <q-icon :name="chgPwdDta.vis ? 'visibility':'visibility_off'"
        class="cursor-pointer" @click="chgPwdDta.vis=!chgPwdDta.vis"></q-icon>
     </template>
    </q-input>
   </q-card-section>
   <q-card-actions align="right" class="text-primary">
    <q-btn flat :label="tags.ok" @click="changePwd"></q-btn>
    <q-btn flat :label="tags.cancel" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<register-dialog :tags="tags" ref="regDlg"></register-dialog>
<component-alert-dialog :title="tags.alert" :errMsgs="tags.errMsgs" :close="tags.close" ref="alertDlg"></component-alert-dialog>
<component-process-dialog ref="procDlg"></component-process-dialog>
`}